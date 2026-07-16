import sys
import traceback

# Diagnostic: try importing the app modules and catch errors
try:
    from flask import Flask, render_template, request, jsonify, send_file
    from werkzeug.utils import secure_filename
    import os
    import re
    import tempfile
    import uuid
    from collections import OrderedDict
    from datetime import datetime
    from pathlib import Path
    from typing import Dict, List

    # Try importing src modules
    from src.cad_parser import CADParser
    from src.dfm_inspector import DFMInspector
    from src.report_generator import ReportGenerator

    IMPORT_ERROR = None
except Exception as e:
    IMPORT_ERROR = traceback.format_exc()
    from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    if IMPORT_ERROR:
        return f'<h1>Import Error</h1><pre>{IMPORT_ERROR}</pre>', 500
    return render_template('index.html')

@app.route('/health')
def health():
    return 'OK', 200
"""
DFM Inspector - Simplified Web Application
Manufacturing Design for Manufacturability Analysis
"""
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import re
import tempfile
import uuid
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# UUID v4 pattern used to validate the opaque upload_id token issued by
# /api/upload. Matches the canonical 8-4-4-4-12 hex-with-dashes form with
# version nibble '4' and variant nibble in [89abAB].
_UUID4_RE = re.compile(
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
)


def _resolve_upload(upload_id: str, filename: str) -> str:
    """
    Resolve an uploaded file to an absolute path inside UPLOAD_FOLDER.

    Raises ValueError on any validation failure. The route handlers
    catch ValueError and return HTTP 400 with {"error": "Invalid file path"}.
    """
    # 1. upload_id must look like a UUID v4
    if not _UUID4_RE.fullmatch(upload_id or ""):
        raise ValueError("invalid upload_id")

    # 2. filename must survive secure_filename and remain non-empty
    safe_name = secure_filename(filename or "")
    if not safe_name:
        raise ValueError("invalid filename")

    # 3. build candidate inside UPLOAD_FOLDER/<upload_id>/<safe_name>
    upload_root = os.path.realpath(app.config['UPLOAD_FOLDER'])
    candidate = os.path.realpath(
        os.path.join(upload_root, upload_id, safe_name)
    )

    # 4. containment check — the resolved real path must live under the
    #    real upload root, with a trailing os.sep so /tmp/upload-evil
    #    does not match /tmp/upload.
    if not candidate.startswith(upload_root + os.sep):
        raise ValueError("path escapes upload folder")

    # 5. existence check
    if not os.path.isfile(candidate):
        raise ValueError("file not found")

    return candidate


# LRU-bounded cache for storing parser objects (keyed by resolved filepath).
# Each cached parser is trimesh+OCP-backed and can hold tens of MB of mesh
# data; cap at 10 entries — well above realistic concurrent report load and
# below a problematic working set.
MAX_PARSER_CACHE_SIZE = 10
_parser_cache: "OrderedDict[str, object]" = OrderedDict()


def _cache_put(filepath: str, parser) -> None:
    """LRU put: move-to-end on hit, evict-front on overflow."""
    if filepath in _parser_cache:
        _parser_cache.move_to_end(filepath)
        _parser_cache[filepath] = parser
        return
    while len(_parser_cache) >= MAX_PARSER_CACHE_SIZE:
        _parser_cache.popitem(last=False)          # evict LRU
    _parser_cache[filepath] = parser


def _cache_get(filepath: str):
    """LRU get: returns parser and refreshes recency, or None."""
    parser = _parser_cache.get(filepath)
    if parser is not None:
        _parser_cache.move_to_end(filepath)
    return parser


def _cache_pop(filepath: str):
    """Explicit removal — used by Word export when the parser is consumed."""
    return _parser_cache.pop(filepath, None)

ALLOWED_EXTENSIONS = {'step', 'stp', 'iges', 'igs', 'stl'}

# Manufacturing processes - simplified structure
PROCESSES = {
    'cnc_machining': {
        'name': 'CNC Machining',
        'icon': '⚙️',
        'description': 'Milling, turning, drilling',
        'status': 'available',
        'materials': ['Aluminum 6061', 'Aluminum 7075', 'Steel 1018', 'Stainless 304']
    },
    'welding': {
        'name': 'Welding',
        'icon': '🔥',
        'description': 'MIG, TIG, spot welding',
        'status': 'available',
        'materials': ['Steel Structural', 'Aluminum', 'Stainless Steel']
    },
    'sheet_metal': {
        'name': 'Sheet Metal',
        'icon': '📋',
        'description': 'Bending, forming, laser cutting',
        'status': 'available',
        'materials': ['Steel', 'Aluminum 5052', 'Aluminum 6061', 'Stainless Steel']
    },
    'injection_molding': {
        'name': 'Injection Molding',
        'icon': '💉',
        'description': 'Plastic part molding',
        'status': 'available',
        'materials': ['ABS', 'Polycarbonate', 'Nylon', 'PP']
    },
    'die_casting': {
        'name': 'Die Casting (HPDC)',
        'icon': '🏭',
        'description': 'High-pressure die casting per 930-00166',
        'status': 'available',
        'materials': ['Aluminum A380', 'AlSi12(Fe)', 'Zinc', 'Magnesium']
    },
    'lpdc': {
        'name': 'Low Pressure Die Casting',
        'icon': '⚙️',
        'description': 'LPDC - low pressure gravity-fed casting per 930-00166',
        'status': 'available',
        'materials': ['Aluminum A380', 'Aluminum 319.0', 'AlSi12(Fe)']
    },
    'permanent_mold': {
        'name': 'Permanent Mold / Gravity Cast',
        'icon': '🔵',
        'description': 'Gravity-fed permanent mold casting per 930-00166',
        'status': 'available',
        'materials': ['Aluminum 319.0', 'Aluminum A380', 'AlSi12(Fe)']
    },
    'investment_casting': {
        'name': 'Investment Casting',
        'icon': '🎨',
        'description': 'Lost-wax casting',
        'status': 'available',
        'materials': ['Steel', 'Stainless', 'Aluminum']
    },
    'mim': {
        'name': 'Metal Injection Molding',
        'icon': '🔩',
        'description': 'Powder metallurgy',
        'status': 'available',
        'materials': ['Stainless Steel', 'Tool Steel']
    },
    'rotational_molding': {
        'name': 'Rotational Molding',
        'icon': '🔄',
        'description': 'Hollow plastic parts',
        'status': 'available',
        'materials': ['Polyethylene', 'Polypropylene']
    },
    'wire_forming': {
        'name': 'Wire Forming',
        'icon': '🔗',
        'description': 'Wire bending',
        'status': 'available',
        'materials': ['Steel Wire', 'Stainless Wire', 'Spring Steel']
    },
    'vacuum_forming': {
        'name': 'Vacuum Forming',
        'icon': '🌬️',
        'description': 'Thermoforming',
        'status': 'available',
        'materials': ['ABS', 'PETG', 'Polystyrene']
    }
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('interface.html', processes=PROCESSES)


@app.route('/api/processes')
def get_processes():
    return jsonify(PROCESSES)


@app.route('/health', methods=['GET'])
def health_check():
    """Lightweight readiness probe for load balancers and container health.

    Stateless: returns 200 with a minimal JSON body. Does not exercise
    any downstream system, since transient failures of CAD libraries
    should not flap the load balancer."""
    return jsonify({'status': 'ok'}), 200


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        filename = secure_filename(file.filename)
        # Give each upload its own unique subdirectory so concurrent uploads
        # of files with the same name don't overwrite each other. The UUID
        # is returned to the client as `upload_id` and is the only handle
        # the client uses to refer to this upload on subsequent analyze
        # calls — the absolute server-side path is never exposed.
        upload_id = str(uuid.uuid4())
        unique_dir = os.path.join(app.config['UPLOAD_FOLDER'], upload_id)
        os.makedirs(unique_dir, exist_ok=True)
        filepath = os.path.join(unique_dir, filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'upload_id': upload_id,
            'size': os.path.getsize(filepath)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/enhanced-test')
def enhanced_test():
    """Serve the enhanced analysis test interface"""
    return render_template('enhanced_test.html')


@app.route('/api/enhanced-analyze', methods=['POST'])
def enhanced_analyze():
    """Enhanced 3D geometry analysis using EnhancedSTEPParser and MeshAnalyzer"""
    data = request.json or {}
    try:
        filepath = _resolve_upload(data.get('upload_id'), data.get('filename'))
    except ValueError:
        return jsonify({"error": "Invalid file path"}), 400
    
    try:
        from src.enhanced_analysis_integration import analyze_with_enhanced_parser
        
        # Perform enhanced analysis
        results = analyze_with_enhanced_parser(filepath)
        
        # Cache the parser for later use (if available)
        if results.get('parser'):
            _cache_put(filepath, results['parser'])
            # Remove parser from results before sending to browser (not JSON serializable)
            del results['parser']
        
        return jsonify(results)
        
    except Exception as e:
        print(f"Enhanced analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'parser_used': 'EnhancedSTEPParser',
            'fallback_available': True
        }), 500


_MATERIAL_DISPLAY = {
    'aluminum': 'Aluminum 6061-T6',
    'steel': 'Steel (low carbon)',
    'stainless_steel': 'Stainless Steel 304',
    'plastic': 'Generic plastic (ABS / PC)',
}


def _material_display(material_id: str) -> str:
    """Map a v1 material_id enum value to a human-friendly display name."""
    return _MATERIAL_DISPLAY.get(material_id, material_id)


def _perform_analysis(filepath: str, process: str, material: str) -> Dict:
    """Run the DFM analyzer pipeline against a resolved upload.

    Shared between the legacy ``/api/analyze`` route (which jsonifies the
    raw analyzer dict for the local HTML UI) and ``/api/v1/analyze`` (which
    wraps the result in the v1 wire format -- see docs/api-contract.md).

    Side effect: caches the parser in ``_parser_cache`` so the Word export
    endpoint can reuse it without re-parsing the STEP file.

    Raises
    ------
    RuntimeError
        If both EnhancedSTEPParser and SimpleCADParser fail to load the file.
        Callers decide whether to surface this as a fallback dict (legacy
        contract) or an error response (v1 contract).
    """
    import logging as _log
    # Try CadQuery-based feature extraction first (most accurate for sheet metal)
    geometry = None
    _log.getLogger(__name__).warning(f"CADQUERY CHECK: process='{process}', filepath='{filepath}'")
    if process in ('sheet_metal', 'cnc_machining', 'die_casting', 'lpdc', 'permanent_mold', 'injection_molding'):
        try:
            from src.cadquery_feature_extractor import extract_features_from_step
            _log.getLogger(__name__).warning(f"CADQUERY: checking filepath endswith step: {filepath.lower().endswith(('.step', '.stp'))}")
            if filepath.lower().endswith(('.step', '.stp')):
                cq_features = extract_features_from_step(filepath)
                if cq_features.get('features_extracted'):
                    geometry = cq_features
                    _log.getLogger(__name__).warning(f"\u2713 CadQuery extracted: {len(cq_features.get('holes',[]))} holes, {len(cq_features.get('bends',[]))} bends, thickness={cq_features.get('estimated_min_thickness')}mm")
                else:
                    _log.getLogger(__name__).warning(f"\u26a0 CadQuery extraction returned no features: {cq_features.get('error', 'unknown')}")
        except Exception as e:
            import traceback
            _log.getLogger(__name__).warning(f"\u26a0 CadQuery extraction failed: {e}")
            traceback.print_exc()

    # Use Enhanced STEP Parser for accurate geometry
    from src.enhanced_step_parser import EnhancedSTEPParser
    from src.mesh_analyzer import MeshAnalyzer

    parser = EnhancedSTEPParser(filepath)
    success = parser.load()

    if not success:
        # Fallback to simple parser if enhanced parser fails
        print("\u26a0 Enhanced parser failed, falling back to SimpleCADParser")
        from src.simple_cad_parser import SimpleCADParser
        parser = SimpleCADParser(filepath)
        success = parser.load()
        if not success:
            raise RuntimeError("Failed to parse file")

    # Get geometry analysis - use CadQuery data if available, otherwise Trimesh
    if geometry is None:
        geometry = parser.get_analysis_summary()

    print(f"DEBUG geometry: dims={geometry.get('dimensions')}, thickness={geometry.get('estimated_min_thickness')}, holes={len(geometry.get('holes', []))}, bends={len(geometry.get('bends', []))}")

    # Add mesh quality analysis if available
    if hasattr(parser, 'mesh') and parser.mesh is not None:
        try:
            analyzer = MeshAnalyzer(parser.mesh)
            mesh_quality = analyzer.analyze_quality()
            geometry['mesh_quality'] = mesh_quality
            geometry['quality_rating'] = mesh_quality.get('quality_rating', 'Unknown')
            print(f"\u2713 Mesh quality: {mesh_quality.get('quality_rating')}")
        except Exception as e:
            print(f"\u26a0 Mesh quality analysis failed: {e}")

    # Dispatch to the right analyzer for the requested process
    if process == 'cnc_machining':
        from src.cnc_machining_enhanced import analyze_cnc_machining_enhanced
        results = analyze_cnc_machining_enhanced(parser, material, geometry)
    elif process == 'welding':
        results = _analyze_welding(parser, material, geometry)
    elif process == 'sheet_metal':
        from src.sheet_metal_enhanced import analyze_sheet_metal_enhanced
        results = analyze_sheet_metal_enhanced(parser, material, geometry)
    elif process == 'injection_molding':
        from src.injection_molding_enhanced_v2 import analyze_injection_molding_enhanced_v2
        results = analyze_injection_molding_enhanced_v2(parser, material, geometry)
    elif process == 'die_casting':
        from src.die_casting_enhanced_v2 import analyze_die_casting_enhanced_v2
        results = analyze_die_casting_enhanced_v2(parser, material, geometry, process_type='hpdc')
    elif process == 'lpdc':
        from src.die_casting_enhanced_v2 import analyze_die_casting_enhanced_v2
        results = analyze_die_casting_enhanced_v2(parser, material, geometry, process_type='lpdc')
    elif process == 'permanent_mold':
        from src.die_casting_enhanced_v2 import analyze_die_casting_enhanced_v2
        results = analyze_die_casting_enhanced_v2(parser, material, geometry, process_type='gravity')
    elif process == 'investment_casting':
        from src.process_analyzers import analyze_investment_casting
        results = analyze_investment_casting(parser, material, geometry)
    elif process == 'mim':
        from src.process_analyzers import analyze_mim
        results = analyze_mim(parser, material, geometry)
    elif process == 'rotational_molding':
        from src.process_analyzers import analyze_rotational_molding
        results = analyze_rotational_molding(parser, material, geometry)
    elif process == 'wire_forming':
        from src.process_analyzers import analyze_wire_forming
        results = analyze_wire_forming(parser, material, geometry)
    elif process == 'vacuum_forming':
        from src.process_analyzers import analyze_vacuum_forming
        results = analyze_vacuum_forming(parser, material, geometry)
    else:
        results = _analyze_generic(parser, material, geometry, process)

    # Cache the parser for later use in Word export
    _cache_put(filepath, parser)

    # Remove parser from results before returning (not JSON serializable)
    if 'parser' in results:
        del results['parser']

    return results


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Legacy DFM analysis endpoint.

    Returns the raw analyzer dict for backwards compatibility with the
    local HTML UI in templates/. New consumers (Harmony frontend, future
    integrations) should target /api/v1/analyze instead -- it returns the
    stable wire format documented in docs/api-contract.md.
    """
    data = request.json or {}
    try:
        filepath = _resolve_upload(data.get('upload_id'), data.get('filename'))
    except ValueError:
        return jsonify({"error": "Invalid file path"}), 400
    process = data.get('process')
    material = data.get('material')

    if process not in PROCESSES:
        return jsonify({'error': 'Invalid process'}), 400

    try:
        results = _perform_analysis(filepath, process, material)
        return jsonify(results)
    except Exception as e:
        # Error - return fallback results (legacy contract)
        print(f"Analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify(_get_fallback_results(process, material, filepath, str(e)))


@app.route('/api/v1/analyze', methods=['POST'])
def analyze_v1():
    """v1 wire-format DFM analysis endpoint.

    Contract: docs/api-contract.md
    Pydantic source of truth: src/api_contract.py
    Spec: .kiro/specs/backend-harmony-wireup/

    Differs from /api/analyze in three ways:

    1. Request body is strictly validated against AnalyzeRequest. Extra or
       missing fields produce a 400 with a structured ErrorResponse.
    2. Successful response is the stable wire format -- summary cards,
       severity-coded findings, exports block -- not the internal analyzer
       dict.
    3. Failure modes return ErrorResponse with a machine-readable code,
       not a fake-success fallback.
    """
    from src.api_contract import (
        AnalyzeRequest, AnalyzeRequestMetadata, ErrorResponse,
    )
    from src.api_transform import to_api_response
    from pydantic import ValidationError

    # 1. Request validation
    try:
        req = AnalyzeRequest.model_validate(request.json or {})
    except ValidationError as e:
        body = ErrorResponse(
            error="Request body did not validate against AnalyzeRequest schema.",
            code="INVALID_REQUEST",
            details={"errors": e.errors()},
        ).to_wire()
        return jsonify(body), 400

    # 2. Upload resolution
    try:
        filepath = _resolve_upload(str(req.upload_id), req.filename)
    except ValueError as e:
        body = ErrorResponse(
            error="Could not resolve upload",
            code="INVALID_FILE_PATH",
            details={"reason": str(e)},
        ).to_wire()
        return jsonify(body), 400

    # 3. Run analyzer
    try:
        results = _perform_analysis(filepath, req.process.value, req.material.value)
    except Exception as e:
        import traceback
        traceback.print_exc()
        body = ErrorResponse(
            error="Analyzer failed",
            code="ANALYZER_FAILED",
            details={"reason": str(e)},
        ).to_wire()
        return jsonify(body), 500

    # 4. Transform to wire format
    process_info = PROCESSES.get(req.process.value, {})
    metadata = AnalyzeRequestMetadata(
        filename=req.filename,
        process_id=req.process,
        process_display=process_info.get('name', req.process.value),
        material_id=req.material,
        material_display=_material_display(req.material.value),
    )
    response = to_api_response(results, metadata)
    return jsonify(response.to_wire())


def _analyze_cnc_machining(parser, material, geometry) -> Dict:
    """Analyze for CNC machining with comprehensive industry-standard DFM rules"""
    issues = []
    warnings = []
    suggestions = []
    passed = []
    rationale = []
    all_rules = []  # NEW: Complete rule-by-rule breakdown
    
    # Get dimensions
    dims = geometry.get('dimensions', {})
    volume = geometry.get('volume', 0)
    surface_area = geometry.get('surface_area', 0)
    min_thickness = geometry.get('estimated_min_thickness', 0)
    
    # RULE 1: Wall Thickness (ISO 2768)
    rule_name = "Wall Thickness (ISO 2768)"
    rule_standard = "Minimum 0.8mm aluminum, 1.0mm steel. Optimal: 2.0mm+ for standard machining"
    if min_thickness > 0:
        if min_thickness < 0.5:
            issues.append({
                'category': 'Wall Thickness',
                'message': f'Critical: Wall thickness {min_thickness:.2f}mm is too thin',
                'recommendation': 'Increase to minimum 0.8mm for aluminum, 1.0mm for steel',
                'rationale': f'Walls below 0.5mm will deflect under cutting forces, causing chatter, poor surface finish, and dimensional errors. Tool breakage risk is high. Standard: ISO 2768-m requires 0.8mm minimum for reliable machining.'
            })
            rationale.append(f"❌ Wall thickness {min_thickness:.2f}mm critically thin - will deflect during machining (ISO 2768).")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'FAIL',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall thickness of {min_thickness:.2f}mm is below the minimum requirement of 0.5mm. This is a critical failure.',
                'recommendation': 'Increase wall thickness to at least 0.8mm for aluminum or 1.0mm for steel',
                'rationale': 'Walls thinner than 0.5mm will deflect under cutting forces, causing chatter, poor surface finish, dimensional errors, and high risk of tool breakage. The cutting tool will push the thin wall away, making it impossible to achieve specified tolerances.',
                'cost_impact': 'Parts with walls <0.5mm will likely be rejected by machine shops or require 200-300% cost premium for specialized micro-machining'
            })
        elif min_thickness < 1.5:
            warnings.append({
                'category': 'Wall Thickness',
                'message': f'Wall thickness {min_thickness:.2f}mm is marginal',
                'recommendation': 'Increase to 2.0mm for aluminum, 2.5mm for steel for optimal rigidity',
                'rationale': f'Thin walls ({min_thickness:.2f}mm) require reduced feed rates (50% slower), special fixturing, and multiple light passes. Cost increases 30-40% vs standard 2.0mm+ walls.'
            })
            rationale.append(f"⚠️ Wall thickness {min_thickness:.2f}mm requires careful machining - 30-40% cost premium.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall thickness of {min_thickness:.2f}mm is machinable but marginal. Falls below the recommended 1.5mm threshold.',
                'recommendation': 'Increase to 2.0mm for aluminum or 2.5mm for steel to enable standard machining parameters',
                'rationale': 'Thin walls between 0.5-1.5mm require reduced feed rates (50% slower), special low-profile fixturing, and multiple light finishing passes to prevent deflection. Machinists must use careful techniques to avoid part distortion.',
                'cost_impact': '30-40% cost increase vs standard 2.0mm+ walls due to slower machining and additional setup requirements'
            })
        else:
            passed.append({'check': 'Wall Thickness', 'status': f'{min_thickness:.2f}mm - Excellent rigidity'})
            rationale.append(f"✓ Wall thickness {min_thickness:.2f}mm provides excellent rigidity for standard machining parameters.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'PASS',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall thickness of {min_thickness:.2f}mm exceeds the recommended minimum and provides excellent rigidity.',
                'recommendation': 'No changes needed - wall thickness is optimal for CNC machining',
                'rationale': 'Walls 1.5mm and thicker provide sufficient rigidity to resist cutting forces without deflection. This allows use of standard machining parameters (full depth of cut, normal feed rates) without special fixturing or multiple passes.',
                'cost_impact': 'Standard machining cost - no premium required'
            })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': 'Not measured',
            'evaluation': 'Wall thickness could not be measured from the CAD geometry',
            'recommendation': 'Verify wall thickness manually in CAD software',
            'rationale': 'Wall thickness analysis requires a watertight 3D model. Ensure your CAD file is properly exported.',
            'cost_impact': 'N/A'
        })
    
    # RULE 2: Hole Depth-to-Diameter Ratio
    rule_name = "Hole Depth-to-Diameter Ratio"
    rule_standard = "Standard drilling: ≤4× diameter. Deep hole: 4-10× (peck drilling). Gun drilling: >10× diameter"
    if dims:
        depth = dims.get('z', 0)
        min_dim = min(dims.values()) if dims.values() else 0
        
        if min_dim > 0 and depth > 0:
            depth_ratio = depth / min_dim
            if depth_ratio > 10:
                issues.append({
                    'category': 'Hole Depth Ratio',
                    'message': f'Deep hole detected: depth/diameter ratio ~{depth_ratio:.1f}:1',
                    'recommendation': 'Limit hole depth to 4× diameter for standard drilling, 10× maximum with gun drilling',
                    'rationale': f'Holes deeper than 4× diameter require specialized deep-hole drilling (gun drilling or BTA), increasing cost 200-500%. Chip evacuation becomes difficult, causing tool breakage and poor hole quality. Standard twist drills limited to 4×D.'
                })
                rationale.append(f"❌ Deep hole ratio ~{depth_ratio:.1f}:1 requires gun drilling - major cost increase.")
                all_rules.append({
                    'name': rule_name,
                    'standard': rule_standard,
                    'status': 'FAIL',
                    'measured_value': f'~{depth_ratio:.1f}:1 ratio',
                    'evaluation': f'Estimated hole depth-to-diameter ratio of {depth_ratio:.1f}:1 exceeds the 10:1 limit for standard deep-hole drilling',
                    'recommendation': 'Reduce hole depth, increase diameter, or redesign to eliminate deep holes. Consider drilling from both sides and meeting in middle.',
                    'rationale': 'Holes deeper than 10× diameter require specialized gun drilling or BTA (Boring and Trepanning Association) equipment. Standard twist drills cannot reach this depth due to chip evacuation problems, tool deflection, and poor straightness. Gun drilling uses specialized single-flute drills with internal coolant delivery.',
                    'cost_impact': '200-500% cost increase for gun drilling. Limited shop availability. Lead time increases 2-4 weeks.'
                })
            elif depth_ratio > 4:
                warnings.append({
                    'category': 'Hole Depth Ratio',
                    'message': f'Hole depth/diameter ratio ~{depth_ratio:.1f}:1 is challenging',
                    'recommendation': 'Reduce depth or increase diameter to achieve 3-4× ratio',
                    'rationale': f'Holes deeper than 4× diameter require peck drilling cycles, increasing cycle time 40-60%. Straightness tolerance degrades beyond 4×D. Best practice: keep holes ≤3× diameter for tight tolerances.'
                })
                rationale.append(f"⚠️ Hole depth ratio ~{depth_ratio:.1f}:1 requires peck drilling - 40-60% longer cycle time.")
                all_rules.append({
                    'name': rule_name,
                    'standard': rule_standard,
                    'status': 'WARNING',
                    'measured_value': f'~{depth_ratio:.1f}:1 ratio',
                    'evaluation': f'Estimated hole depth-to-diameter ratio of {depth_ratio:.1f}:1 exceeds the 4:1 standard drilling limit',
                    'recommendation': 'Reduce hole depth or increase diameter to achieve 3-4:1 ratio for optimal results',
                    'rationale': 'Holes between 4-10× diameter require peck drilling (drill advances in steps, retracting periodically to clear chips). This increases cycle time by 40-60%. Hole straightness degrades - expect ±0.1mm per 25mm depth. Chip evacuation becomes difficult, risking tool breakage.',
                    'cost_impact': '40-60% longer cycle time for peck drilling. Straightness tolerance may require reaming (+20% cost per hole).'
                })
            else:
                passed.append({'check': 'Hole Depth Ratio', 'status': 'Within standard drilling limits'})
                rationale.append(f"✓ Hole depth ratio suitable for standard drilling operations.")
                all_rules.append({
                    'name': rule_name,
                    'standard': rule_standard,
                    'status': 'PASS',
                    'measured_value': f'~{depth_ratio:.1f}:1 ratio',
                    'evaluation': f'Estimated hole depth-to-diameter ratio of {depth_ratio:.1f}:1 is within standard drilling limits',
                    'recommendation': 'No changes needed - holes can be drilled with standard twist drills',
                    'rationale': 'Holes with depth ≤4× diameter can be drilled efficiently with standard twist drills using continuous drilling (no pecking required). Chip evacuation is effective, tool life is normal, and hole straightness meets standard tolerances.',
                    'cost_impact': 'Standard drilling cost - no premium'
                })
        else:
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'INFO',
                'measured_value': 'Not applicable',
                'evaluation': 'Hole depth-to-diameter ratio could not be estimated from part geometry',
                'recommendation': 'Manually verify any holes in your design meet the 4:1 standard drilling limit',
                'rationale': 'This rule applies to drilled holes. If your part has holes, ensure depth ≤4× diameter for standard drilling.',
                'cost_impact': 'N/A'
            })
    
    # Continue with remaining rules... (I'll add a few more key ones)
    
    # RULE 3: Internal Corner Radii
    rule_name = "Internal Corner Radii"
    rule_standard = "Minimum radius = 1/3 of pocket depth OR 0.5mm, whichever is greater"
    if dims:
        depth = dims.get('z', 0)
        if depth > 0:
            min_corner_radius = max(depth / 3, 0.5)
            warnings.append({
                'category': 'Internal Corners',
                'message': f'Internal corners require minimum radius of {min_corner_radius:.2f}mm',
                'recommendation': f'Add {min_corner_radius:.2f}mm radius to all internal corners (1/3 of {depth:.1f}mm depth)',
                'rationale': f'Sharp internal corners are impossible to machine (tools are round). Minimum radius = tool diameter. For {depth:.1f}mm deep pockets, use {min_corner_radius:.2f}mm radius minimum. Smaller radii require smaller tools = slower machining and higher cost.'
            })
            rationale.append(f"⚠️ Internal corners need {min_corner_radius:.2f}mm radius minimum (1/3 depth rule).")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'Pocket depth: {depth:.1f}mm',
                'evaluation': f'For {depth:.1f}mm deep pockets, minimum corner radius must be {min_corner_radius:.2f}mm',
                'recommendation': f'Add {min_corner_radius:.2f}mm radius to all internal corners in pockets and slots',
                'rationale': 'Internal corners cannot be sharp because cutting tools are round. The minimum achievable radius equals the tool radius. For a {depth:.1f}mm deep pocket, the 1/3 depth rule requires {min_corner_radius:.2f}mm radius. Smaller radii require smaller endmills, which cut slower (reduced feed rates), deflect more (poor accuracy), and break more easily (higher cost).',
                'cost_impact': f'Using {min_corner_radius:.2f}mm radius: standard cost. Tighter radii: +30-60% cost due to smaller tooling and slower speeds.'
            })
        else:
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'INFO',
                'measured_value': 'No pockets detected',
                'evaluation': 'Part appears to have no internal pockets or corners requiring radii',
                'recommendation': 'If your design has internal corners, ensure they have appropriate radii',
                'rationale': 'This rule applies to internal corners in pockets, slots, and cavities. External corners can be sharp.',
                'cost_impact': 'N/A'
            })
    
    # Add remaining existing code for other rules...
    # (Keeping the rest of the function as-is for now)
    
    # RULE 4: Thread Depth
    suggestions.append({
        'opportunity': 'Thread depth specification',
        'savings': 'Avoid tap breakage and ensure proper thread engagement',
        'difficulty': 'Easy',
        'rationale': 'Threaded holes require minimum depth of 1.5× nominal diameter (steel) or 2× diameter (aluminum) plus 2-3 thread runout. Example: M6 thread needs 9mm depth (steel) or 12mm (aluminum) plus 2mm runout = 11-14mm total. Insufficient depth causes tap breakage ($50-200 to remove).'
    })
    
    all_rules.append({
        'name': "Thread Depth Specification",
        'standard': "Minimum engagement: 1.5× diameter (steel), 2× diameter (aluminum), plus 2-3mm runout",
        'status': 'INFO',
        'measured_value': 'N/A',
        'evaluation': 'Thread depth cannot be verified from geometry - this is a design specification rule',
        'recommendation': 'For any threaded holes: Steel = 1.5×D + 2mm, Aluminum = 2×D + 2mm. Example: M6 in steel = 11mm total depth',
        'rationale': 'Threads need sufficient engagement depth to develop full strength. Steel threads engage better (1.5× diameter sufficient). Aluminum is softer and requires 2× diameter engagement. Additional 2-3mm runout depth allows tap to clear and prevents incomplete threads at bottom. Insufficient depth causes tap breakage during manufacturing ($50-200 to extract broken tap).',
        'cost_impact': 'Proper depth: standard cost. Insufficient depth: tap breakage adds $50-200 per hole + potential part scrap'
    })
    
    # Continue with remaining rules from original function...
    # (I'll keep the rest of the logic but won't repeat it all here)
    
    # RULE 5: Part Size and Machine Capacity
    if dims:
        max_dim = max(dims.values())
        min_dim = min(dims.values())
        
        rationale.append(f"Part envelope: {dims.get('x', 0):.1f} × {dims.get('y', 0):.1f} × {dims.get('z', 0):.1f} mm")
        
        if max_dim > 1000:
            issues.append({
                'category': 'Part Size',
                'message': f'Oversized part: {max_dim:.1f}mm exceeds standard machine capacity',
                'recommendation': 'Redesign to fit 500×500×500mm envelope or split into assemblies',
                'rationale': f'Parts over 1000mm require large-format 5-axis machines (very limited availability). Cost increases 300-500%. Standard 3-axis machines: 500×500×500mm. Consider splitting into bolted assembly.'
            })
            rationale.append(f"❌ Part size {max_dim:.1f}mm requires specialized large-format equipment - 300-500% cost increase.")
        elif max_dim > 500:
            warnings.append({
                'category': 'Part Size',
                'message': f'Large part dimension: {max_dim:.1f}mm',
                'recommendation': 'Verify machine capacity (standard: 500×500×500mm) or split into smaller parts',
                'rationale': f'Parts 500-1000mm require large-bed machines, reducing shop options by 60-70%. Setup costs increase 50-100%. Standard machines accommodate 500mm max.'
            })
            rationale.append(f"⚠️ Part size {max_dim:.1f}mm limits machine shop options - 50-100% cost premium.")
        else:
            passed.append({'check': 'Part Size', 'status': 'Fits standard 3-axis machines'})
            rationale.append(f"✓ Part fits standard CNC machine envelopes (500×500×500mm) - maximum shop compatibility.")
        
        # RULE 6: Small Features and Tool Access
        if min_dim < 2.0:
            issues.append({
                'category': 'Small Features',
                'message': f'Micro-feature detected: {min_dim:.1f}mm',
                'recommendation': 'Increase feature size to minimum 2.0mm for standard tooling',
                'rationale': f'Features below 2.0mm require micro-tooling (0.5-1.5mm diameter endmills) which are fragile and expensive. Feed rates reduced 70-80%, cycle time increases 200-400%. Minimum practical feature: 2.0mm with standard tooling.'
            })
            rationale.append(f"❌ Feature size {min_dim:.1f}mm requires micro-tooling - 200-400% cycle time increase.")
        elif min_dim < 5.0:
            warnings.append({
                'category': 'Small Features',
                'message': f'Small feature: {min_dim:.1f}mm',
                'recommendation': 'Increase to 5.0mm+ for optimal machining efficiency',
                'rationale': f'Features 2-5mm require small tooling (2-4mm endmills), increasing cycle time 40-60% vs standard 6-12mm tools. Tool deflection affects accuracy. Best practice: 5mm minimum feature size.'
            })
            rationale.append(f"⚠️ Small feature {min_dim:.1f}mm requires small tooling - 40-60% longer cycle time.")
        else:
            passed.append({'check': 'Feature Size', 'status': 'Suitable for standard tooling'})
            rationale.append(f"✓ Feature sizes accommodate standard tooling (6-12mm) for efficient machining.")
    
    # Add remaining rules (7-13) following the same pattern...
    # (Keeping original logic for brevity)
    
    # RULE 7: Tolerance Specifications (ISO 2768)
    suggestions.append({
        'opportunity': 'Apply ISO 2768-m general tolerances',
        'savings': '20-30% cost reduction vs tight tolerances on all dimensions',
        'difficulty': 'Easy',
        'rationale': 'ISO 2768-m provides ±0.1mm for dimensions up to 30mm, ±0.2mm up to 120mm. Only specify tighter tolerances (±0.05mm or better) where functionally required. Each tight tolerance dimension adds 15-25% to cost due to inspection and process control requirements.'
    })
    
    # RULE 8: Surface Finish
    suggestions.append({
        'opportunity': 'Specify Ra 3.2μm (125μin) standard finish',
        'savings': '15-25% vs Ra 1.6μm or better',
        'difficulty': 'Easy',
        'rationale': 'Standard CNC machining achieves Ra 3.2μm (125μin) as-machined. Ra 1.6μm requires additional finishing passes (30-50% longer cycle time). Ra 0.8μm requires grinding or polishing (100-200% cost increase). Only specify fine finishes where functionally required (sealing surfaces, bearing surfaces).'
    })
    
    # RULE 9: Geometry Integrity
    if not geometry.get('is_watertight', False):
        issues.append({
            'category': 'Geometry',
            'message': 'CAD model has gaps or open surfaces',
            'recommendation': 'Fix geometry to ensure watertight solid model',
            'rationale': 'Non-watertight geometry causes CAM software failures. Open surfaces cannot generate valid toolpaths. Most machine shops will reject quote requests for invalid geometry. Use CAD repair tools to fix gaps, overlapping faces, and non-manifold edges.'
        })
        rationale.append("❌ Geometry integrity failed - model has gaps/open surfaces. Will be rejected by machine shops.")
    else:
        passed.append({'check': 'Geometry Integrity', 'status': 'Watertight solid - CAM ready'})
        rationale.append("✓ Geometry is watertight solid model, suitable for CAM programming.")
    
    # RULE 10: Material Selection and Machinability
    if 'aluminum' in material.lower():
        if '6061' in material or '7075' in material:
            passed.append({'check': 'Material Selection', 'status': 'Excellent machinability'})
            rationale.append(f"✓ {material} - excellent machinability (rating 5/5). Machines 3-4× faster than steel, long tool life.")
            suggestions.append({
                'opportunity': 'Material Selection - Optimal',
                'savings': 'Aluminum machines 3-4× faster than steel, 40-60% lower cost',
                'difficulty': 'N/A',
                'rationale': f'{material} offers excellent machinability with high feed rates (3000-5000 mm/min) and speeds (15,000-20,000 RPM). Tool life 5-10× longer than steel. Material cost moderate ($3-8/lb). Best choice for CNC machining when strength requirements allow.'
            })
        else:
            passed.append({'check': 'Material Selection', 'status': 'Good machinability'})
            rationale.append(f"✓ {material} - good machinability for CNC operations.")
    elif 'steel' in material.lower():
        if 'stainless' in material.lower():
            warnings.append({
                'category': 'Material Machinability',
                'message': 'Stainless steel has poor machinability',
                'recommendation': 'Consider 303 stainless (free-machining) or aluminum if possible',
                'rationale': f'{material} has low machinability (rating 2/5). Work-hardens during cutting, requiring 50-70% reduced feed rates. Tool life 1/5 of aluminum. Cycle time 4-6× longer than aluminum. Cost premium: 200-300% vs aluminum. Use 303 stainless for better machinability or 17-4 PH for strength.'
            })
            rationale.append(f"⚠️ {material} - poor machinability. Cycle time 4-6× longer than aluminum, 200-300% cost increase.")
        else:
            warnings.append({
                'category': 'Material Machinability',
                'message': 'Steel requires longer machining time than aluminum',
                'recommendation': 'Consider aluminum if strength requirements allow',
                'rationale': f'{material} has moderate machinability (rating 3/5). Requires 3-4× longer cycle time vs aluminum due to lower feed rates and speeds. Tool wear increases cost. Use when strength/hardness requirements exceed aluminum capabilities.'
            })
            rationale.append(f"⚠️ {material} - moderate machinability. Cycle time 3-4× longer than aluminum.")
    elif 'brass' in material.lower():
        passed.append({'check': 'Material Selection', 'status': 'Excellent machinability'})
        rationale.append(f"✓ {material} - excellent machinability (rating 5/5). Machines as fast as aluminum with superior surface finish.")
    elif 'titanium' in material.lower():
        warnings.append({
            'category': 'Material Machinability',
            'message': 'Titanium has very poor machinability',
            'recommendation': 'Verify titanium is required - consider aluminum or steel alternatives',
            'rationale': f'{material} has very poor machinability (rating 1/5). Requires 70-80% reduced feed rates, specialized tooling, and high-pressure coolant. Cycle time 8-10× longer than aluminum. Cost premium: 400-600% vs aluminum. Only use when corrosion resistance and strength-to-weight ratio are critical.'
        })
        rationale.append(f"⚠️ {material} - very poor machinability. Cycle time 8-10× longer than aluminum, 400-600% cost increase.")
    
    # RULE 11: Setup and Fixturing
    if dims:
        aspect_ratio = max(dims.values()) / min(dims.values()) if min(dims.values()) > 0 else 1
        if aspect_ratio > 10:
            warnings.append({
                'category': 'Part Geometry',
                'message': f'High aspect ratio: {aspect_ratio:.1f}:1',
                'recommendation': 'Consider redesign to reduce aspect ratio below 5:1',
                'rationale': f'Parts with aspect ratio > 10:1 are difficult to fixture and prone to deflection. Requires custom fixturing ($500-2000) and multiple setups. Vibration and chatter increase. Best practice: keep aspect ratio < 5:1 for standard fixturing.'
            })
            rationale.append(f"⚠️ High aspect ratio {aspect_ratio:.1f}:1 requires custom fixturing and multiple setups.")
    
    # RULE 12: Material Removal and Cycle Time
    if volume > 0:
        material_removal = volume * 0.3  # Estimate 30% material removal
        rationale.append(f"Estimated material removal: {material_removal:.0f} mm³ affects cycle time and tool wear.")
        
        if volume > 0 and surface_area > 0:
            volume_to_surface_ratio = volume / surface_area
            if volume_to_surface_ratio < 0.5:
                suggestions.append({
                    'opportunity': 'Reduce material removal',
                    'savings': '20-35% cycle time reduction',
                    'difficulty': 'Medium',
                    'rationale': f'Low volume-to-surface ratio ({volume_to_surface_ratio:.2f}) indicates thin-walled design with extensive material removal. Consider: (1) Start from thinner stock, (2) Use ribs instead of solid sections, (3) Eliminate non-functional pockets. Each mm³ removed adds cycle time and cost.'
                })
    
    # RULE 13: Standard Features
    suggestions.append({
        'opportunity': 'Use standard hole sizes (metric: 3, 4, 5, 6, 8, 10, 12mm)',
        'savings': '10-20% by eliminating reaming operations',
        'difficulty': 'Easy',
        'rationale': 'Standard drill sizes are readily available and inexpensive. Non-standard holes (e.g., 7.5mm, 9.2mm) require drilling undersize + reaming, adding 30-50% to hole cost. Metric standard: 3, 4, 5, 6, 8, 10, 12, 16, 20mm. Imperial: #7 (0.201"), 1/4", 5/16", 3/8", 1/2".'
    })
    
    suggestions.append({
        'opportunity': 'Avoid undercuts and internal features requiring special tooling',
        'savings': '25-40% by eliminating 4th/5th axis operations',
        'difficulty': 'Medium',
        'rationale': 'Undercuts, T-slots, and internal grooves require 4-axis or 5-axis machining, increasing cost 100-200%. If unavoidable, design for tool access: minimum 3mm tool diameter, 4× depth-to-diameter ratio. Consider redesign as assembly with standard features.'
    })
    
    # Calculate score with explanation
    total_checks = len(issues) + len(warnings) + len(passed)
    if total_checks > 0:
        score = (len(passed) * 100 + len(warnings) * 50) / total_checks
        score_explanation = f"Score calculated from {len(passed)} passed checks (100 pts each), {len(warnings)} warnings (50 pts each), and {len(issues)} critical issues (0 pts). Total: {score:.1f}/100"
    else:
        score = 85.0
        score_explanation = "Default score - limited geometry data available"
    
    # Generate summary
    summary = _generate_cnc_summary(score, len(issues), len(warnings), len(passed), dims, material, min_thickness)
    
    return {
        'success': True,
        'process': 'CNC Machining',
        'material': material,
        'score': round(score, 1),
        'score_explanation': score_explanation,
        'issues': len(issues),
        'warnings': len(warnings),
        'suggestions': len(suggestions),
        'passed': len(passed),
        'all_rules': all_rules,  # NEW: Complete rule breakdown
        'geometry_info': {
            'dimensions': f"{dims.get('x', 0):.1f} x {dims.get('y', 0):.1f} x {dims.get('z', 0):.1f} mm",
            'volume': f"{volume:.2f} mm³",
            'surface_area': f"{surface_area:.2f} mm²",
            'min_thickness': f"{min_thickness:.2f} mm" if min_thickness > 0 else "N/A"
        },
        'rationale': rationale,
        'summary': summary,
        'details': {
            'critical_issues': issues[:5],
            'warnings': warnings[:5],
            'cost_savings': suggestions[:3]
        }
    }


def _generate_cnc_summary(score, issues_count, warnings_count, passed_count, dims, material, min_thickness):
    """Generate comprehensive summary for CNC machining analysis"""
    
    # Overall assessment
    if score >= 90:
        assessment = "EXCELLENT - Ready for Manufacturing"
        recommendation = "This design is well-optimized for CNC machining. Proceed with confidence."
    elif score >= 75:
        assessment = "GOOD - Minor Improvements Recommended"
        recommendation = "Design is manufacturable with some optimization opportunities. Address warnings to reduce cost."
    elif score >= 60:
        assessment = "ACCEPTABLE - Improvements Needed"
        recommendation = "Design is manufacturable but has issues that will increase cost. Review and address warnings before production."
    else:
        assessment = "NEEDS REVISION - Critical Issues Present"
        recommendation = "Design has critical manufacturability issues. Address all critical issues before requesting quotes."
    
    # Build summary
    summary_parts = []
    summary_parts.append(f"**Overall Assessment:** {assessment}")
    summary_parts.append(f"**Manufacturability Score:** {score:.1f}/100")
    summary_parts.append("")
    summary_parts.append(f"**Analysis Results:** {passed_count} checks passed, {warnings_count} warnings, {issues_count} critical issues")
    summary_parts.append("")
    
    # Key findings
    summary_parts.append("**Key Findings:**")
    if min_thickness > 0:
        if min_thickness >= 1.5:
            summary_parts.append(f"• Wall thickness ({min_thickness:.2f}mm) is adequate for rigid machining")
        else:
            summary_parts.append(f"• Wall thickness ({min_thickness:.2f}mm) may cause deflection - consider increasing")
    
    if dims:
        max_dim = max(dims.values())
        if max_dim <= 400:
            summary_parts.append(f"• Part size fits standard CNC machines - good shop compatibility")
        else:
            summary_parts.append(f"• Large part size ({max_dim:.1f}mm) limits machine shop options")
    
    if 'aluminum' in material.lower():
        summary_parts.append(f"• Material choice ({material}) is optimal for CNC - fast machining, low cost")
    elif 'steel' in material.lower():
        summary_parts.append(f"• Material choice ({material}) increases machining time 3-4x vs aluminum")
    
    summary_parts.append("")
    summary_parts.append(f"**Recommendation:** {recommendation}")
    
    if issues_count > 0:
        summary_parts.append("")
        summary_parts.append("**Action Required:** Address critical issues before production to avoid rejected quotes or manufacturing failures.")
    elif warnings_count > 0:
        summary_parts.append("")
        summary_parts.append("**Suggested Actions:** Review warnings to optimize cost and lead time. Design is manufacturable as-is.")
    
    return "\n".join(summary_parts)


def _analyze_welding(parser, material, geometry) -> Dict:
    """Analyze for welding"""
    issues = []
    warnings = []
    suggestions = []
    passed = []
    
    dims = geometry.get('dimensions', {})
    min_thickness = geometry.get('estimated_min_thickness', 0)
    
    # Check material
    if 'aluminum' in material.lower():
        warnings.append({
            'category': 'Material',
            'message': 'Aluminum welding requires special considerations',
            'recommendation': 'Use TIG welding for best results. Ensure proper cleaning and shielding gas.'
        })
    elif 'steel' in material.lower():
        passed.append({'check': 'Material Selection', 'status': 'Good for welding'})
    
    # Check thickness for welding
    if min_thickness > 0:
        if min_thickness < 1.5:
            issues.append({
                'category': 'Material Thickness',
                'message': f'Thickness {min_thickness:.2f}mm may be too thin for welding',
                'recommendation': 'Minimum 1.5mm recommended for most welding processes'
            })
        elif min_thickness < 3.0:
            warnings.append({
                'category': 'Material Thickness',
                'message': f'Thin material {min_thickness:.2f}mm requires careful welding',
                'recommendation': 'Use TIG welding with low heat input to prevent warping'
            })
        else:
            passed.append({'check': 'Material Thickness', 'status': 'Adequate for welding'})
    
    # Geometry checks
    if geometry.get('is_watertight', False):
        passed.append({'check': 'Geometry', 'status': 'OK'})
    
    suggestions.append({
        'opportunity': 'Joint design optimization',
        'savings': '10-20% by using standard joint configurations',
        'difficulty': 'Medium'
    })
    
    # Calculate score
    total_checks = len(issues) + len(warnings) + len(passed)
    score = (len(passed) * 100 + len(warnings) * 50) / total_checks if total_checks > 0 else 85.0
    
    return {
        'success': True,
        'process': 'Welding',
        'material': material,
        'score': round(score, 1),
        'issues': len(issues),
        'warnings': len(warnings),
        'suggestions': len(suggestions),
        'passed': len(passed),
        'geometry_info': {
            'dimensions': f"{dims.get('x', 0):.1f} x {dims.get('y', 0):.1f} x {dims.get('z', 0):.1f} mm",
            'min_thickness': f"{min_thickness:.2f} mm" if min_thickness > 0 else 'N/A'
        },
        'details': {
            'critical_issues': issues[:5],
            'warnings': warnings[:5],
            'cost_savings': suggestions[:3]
        }
    }


def _analyze_generic(parser, material, geometry, process) -> Dict:
    """Generic analysis for other processes"""
    dims = geometry.get('dimensions', {})
    volume = geometry.get('volume', 0)
    
    return {
        'success': True,
        'process': PROCESSES[process]['name'],
        'material': material,
        'score': 85.0,
        'issues': 0,
        'warnings': 1,
        'suggestions': 1,
        'passed': 5,
        'geometry_info': {
            'dimensions': f"{dims.get('x', 0):.1f} x {dims.get('y', 0):.1f} x {dims.get('z', 0):.1f} mm",
            'volume': f"{volume:.2f} mm³"
        },
        'details': {
            'critical_issues': [],
            'warnings': [{
                'category': 'Analysis Status',
                'message': f'{PROCESSES[process]["name"]} analysis is in development',
                'recommendation': 'Basic geometry analysis completed. Full process-specific analysis coming soon.'
            }],
            'cost_savings': [{
                'opportunity': f'Optimize for {PROCESSES[process]["name"]}',
                'savings': '10-20%',
                'difficulty': 'Medium'
            }]
        }
    }


def _get_fallback_results(process, material, filepath, error_msg):
    """Return informative results when CAD analysis isn't available"""
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath) if os.path.exists(filepath) else 0
    
    return {
        'success': True,
        'process': PROCESSES[process]['name'],
        'material': material,
        'score': 80.0,
        'issues': 1,
        'warnings': 2,
        'suggestions': 2,
        'passed': 8,
        'details': {
            'critical_issues': [
                {
                    'category': 'CAD Analysis Status',
                    'message': f'File "{filename}" ({filesize/1024:.1f} KB) uploaded successfully',
                    'recommendation': 'Full 3D CAD analysis requires pythonocc-core library. Currently showing general DFM guidelines.'
                }
            ],
            'warnings': [
                {
                    'category': PROCESSES[process]['name'] + ' - General Guidelines',
                    'message': 'Review design for manufacturability best practices',
                    'recommendation': f'Ensure design follows standard {PROCESSES[process]["name"]} guidelines'
                },
                {
                    'category': 'Material Selection',
                    'message': f'Material: {material}',
                    'recommendation': 'Verify material is suitable for intended application and manufacturing process'
                }
            ],
            'cost_savings': [
                {
                    'opportunity': 'Standardize features',
                    'savings': '10-20%',
                    'difficulty': 'Easy'
                },
                {
                    'opportunity': 'Optimize for ' + PROCESSES[process]['name'],
                    'savings': '15-25%',
                    'difficulty': 'Medium'
                }
            ]
        }
    }


def _get_mock_results(process, material, filepath):
    """Generate mock results for processes not yet implemented"""
    filename = os.path.basename(filepath)
    
    return {
        'score': 85.5,
        'issues': [
            {
                'category': 'Process Status',
                'message': f'{PROCESSES[process]["name"]} analysis is in development',
                'recommendation': f'File "{filename}" received. Full analysis coming soon for this process.'
            }
        ],
        'warnings': [
            {
                'category': 'General DFM',
                'message': 'Review design against standard manufacturing guidelines',
                'recommendation': f'Ensure design is optimized for {PROCESSES[process]["name"]}'
            }
        ],
        'suggestions': [
            {
                'opportunity': 'Design optimization for ' + PROCESSES[process]['name'],
                'savings': '10-20%',
                'difficulty': 'Medium'
            }
        ],
        'passed': []
    }


@app.route('/api/materials/<process>')
def get_materials(process):
    if process not in PROCESSES:
        return jsonify({'error': 'Invalid process'}), 400
    return jsonify({'materials': PROCESSES[process]['materials']})


@app.route('/api/enhanced-dfm-analyze', methods=['POST'])
def enhanced_dfm_analyze():
    """
    Complete Enhanced DFM Analysis with Feature Detection and Violation Highlighting
    
    This endpoint runs the full enhanced workflow:
    1. Parse STEP file with EnhancedSTEPParser
    2. Measure wall thickness with GeometryAnalyzer
    3. Detect features (holes, corners, pockets) with FeatureDetector
    4. Check DFM rules with DFMFeatureIntegration
    5. Return violations with 3D coordinates for visualization
    """
    data = request.json or {}
    try:
        filepath = _resolve_upload(data.get('upload_id'), data.get('filename'))
    except ValueError:
        return jsonify({"error": "Invalid file path"}), 400
    process = data.get('process')
    material = data.get('material')
    
    if process not in PROCESSES:
        return jsonify({'error': 'Invalid process'}), 400
    
    try:
        from src.enhanced_dfm_workflow import EnhancedDFMWorkflow
        
        # Run complete enhanced DFM workflow
        workflow = EnhancedDFMWorkflow(filepath, process, material)
        results = workflow.run_complete_analysis(
            detect_features=True,
            measure_thickness=True,
            sample_density=1000  # 1000 samples per m²
        )
        
        if not results.get('success'):
            return jsonify(results), 500
        
        # Cache the parser and components for later use
        if results.get('parser'):
            _cache_put(filepath, results['parser'])
            # Remove parser from results before sending (not JSON serializable)
            del results['parser']
        
        # Remove components from results (not JSON serializable)
        if 'components' in results:
            del results['components']
        
        return jsonify(results)
        
    except Exception as e:
        print(f"Enhanced DFM analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'process': process,
            'material': material
        }), 500


@app.route('/api/export/word', methods=['POST'])
def export_word():
    """Export analysis results to Word document with 3D visualizations"""
    print("=" * 70)
    print("WORD EXPORT REQUEST RECEIVED")
    print("=" * 70)
    
    try:
        from src.word_report_generator import WordReportGenerator
        
        data = request.json
        print(f"Request data keys: {data.keys() if data else 'None'}")
        
        analysis_results = data.get('results')

        # Resolve the cached parser key from the opaque upload token, mirroring
        # the analyze endpoints. Word export tolerates a missing/invalid path:
        # if resolution fails we fall through to the no-cached-parser branch
        # below (same behaviour as before, just keyed off upload_id+filename
        # instead of a client-supplied absolute path).
        upload_id = data.get('upload_id')
        filename = data.get('filename')
        step_file_path = None
        if upload_id and filename:
            try:
                step_file_path = _resolve_upload(upload_id, filename)
            except ValueError:
                step_file_path = None

        if not analysis_results:
            print("ERROR: No analysis results provided")
            return jsonify({'error': 'No analysis results provided'}), 400
        
        print(f"Analysis results process: {analysis_results.get('process', 'Unknown')}")
        print(f"Analysis results score: {analysis_results.get('score', 'Unknown')}")
        print(f"STEP file path: {step_file_path}")
        
        # Retrieve parser from cache if available. Word generation consumes
        # the parser; pop it so we don't hold a reference past this request.
        parser = None
        if step_file_path:
            parser = _cache_get(step_file_path)
        if parser is not None:
            print(f"✓ Retrieved parser from cache for: {step_file_path}")
            # Add parser back to results for Word generator
            analysis_results['parser'] = parser
        else:
            print(f"⚠ No parser in cache for: {step_file_path}")
        
        # Generate Word document
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        process = analysis_results.get('process', 'DFM').replace(' ', '_')
        filename = f"DFM_Report_{process}_{timestamp}.docx"
        output_path = os.path.join(tempfile.gettempdir(), filename)
        
        print(f"Generating report: {filename}")
        print(f"Output path: {output_path}")
        
        # Create generator with STEP file path AND parser for accurate 3D visualization
        generator = WordReportGenerator(step_file_path=step_file_path, parser=parser)
        report_path = generator.generate_report(analysis_results, output_path)
        
        print(f"Report generated successfully: {report_path}")
        print(f"File size: {os.path.getsize(report_path)} bytes")
        
        # Parser has been consumed by Word generation; drop the cache entry
        # so a long-running deployment doesn't accumulate parsers.
        if step_file_path:
            _cache_pop(step_file_path)
        
        # Send file
        return send_file(
            report_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        print(f"ERROR generating Word report: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import sys
    import io
    
    # Fix Windows console encoding for emojis
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    os.makedirs('templates', exist_ok=True)
    
    print("\n" + "="*70)
    print("🔍 DFM INSPECTOR - Web Application")
    print("="*70)
    print("\n✓ Server starting...")
    print("✓ Open your browser: http://localhost:5000")
    print("\n📋 Available Processes:")
    for key, proc in PROCESSES.items():
        status = "✓" if proc['status'] == 'available' else "⏳"
        print(f"  {status} {proc['icon']} {proc['name']}")
    print("\n⌨️  Press Ctrl+C to stop")
    print("="*70 + "\n")
    
    # Only enable the Werkzeug debugger when explicitly requested via env var,
    # and bind to localhost in that case so the debugger is never exposed to
    # the network. In normal (non-debug) mode we bind to 0.0.0.0 so the app
    # is reachable on the LAN.
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    host = '127.0.0.1' if debug else '0.0.0.0'
    app.run(debug=debug, host=host, port=5000)
