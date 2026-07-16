# Requirements Document: Enhanced 3D Geometry Analysis and Visualization

## Introduction

The Enhanced 3D Geometry Analysis and Visualization feature addresses critical accuracy issues in the DFM Inspector application. Currently, the system uses estimated geometry measurements (bounding boxes, simplified thickness calculations) that produce false DFM errors and inaccurate visualizations. This feature will implement accurate STEP file parsing, precise mesh analysis, comprehensive feature detection, and enhanced 3D visualization with error highlighting for all DFM failure types.

The feature enables accurate Design for Manufacturability analysis by extracting real geometric measurements from STEP files, detecting manufacturing-critical features (walls, corners, holes, pockets, bosses, ribs), and generating 3D renderings that highlight specific problem areas in red.

## Glossary

- **Geometry_Analyzer**: The system component that extracts and measures geometric features from STEP files and 3D meshes
- **Feature_Detector**: The system component that identifies manufacturing-critical features (walls, holes, pockets, bosses, ribs, fillets, chamfers)
- **STEP_Parser**: The system component that reads and interprets STEP file format data
- **Mesh_Analyzer**: The system component that analyzes triangulated 3D mesh data for measurements
- **DFM_Rule_Engine**: The system component that checks detected features against manufacturing rules
- **Visualization_Engine**: The system component that generates 3D renderings with highlighted problem areas
- **Wall_Thickness**: The minimum distance between opposing surfaces of a part
- **Corner_Radius**: The radius of curvature at internal or external corners
- **Feature**: A geometric element of a part (hole, pocket, boss, rib, fillet, chamfer, wall)
- **DFM_Failure**: A geometric condition that violates manufacturing rules for a specific process
- **Highlight**: Visual indication in red color on 3D rendering showing location of DFM failure
- **Round_Trip_Property**: The property that parsing then printing then parsing produces equivalent result
- **Measurement_Tolerance**: The acceptable deviation between measured and actual dimensions (±0.01mm)

## Requirements

### Requirement 1: Accurate STEP File Parsing

**User Story:** As a DFM engineer, I want the system to accurately parse STEP files and extract real geometric data, so that measurements match what I see in my CAD software.

#### Acceptance Criteria

1. WHEN a STEP file is provided, THE STEP_Parser SHALL extract all geometric entities including surfaces, edges, vertices, and topology
2. WHEN geometric entities are extracted, THE STEP_Parser SHALL preserve dimensional accuracy within ±0.01mm tolerance
3. THE STEP_Parser SHALL extract coordinate data for all vertices in the model
4. THE STEP_Parser SHALL extract surface normal vectors for all faces
5. THE STEP_Parser SHALL extract edge connectivity information
6. IF the STEP file is corrupted or invalid, THEN THE STEP_Parser SHALL return a descriptive error message identifying the specific parsing failure
7. WHEN parsing completes successfully, THE STEP_Parser SHALL provide a data structure containing all extracted geometric entities
8. THE STEP_Parser SHALL support STEP AP203 and AP214 file formats
9. WHEN a STEP file contains assembly data, THE STEP_Parser SHALL extract geometry from all component parts

### Requirement 2: Wall Thickness Measurement

**User Story:** As a DFM engineer, I want the system to measure actual wall thickness from the 3D geometry, so that thin wall violations are detected with real measurements instead of estimates.

#### Acceptance Criteria

1. WHEN a 3D mesh is loaded, THE Geometry_Analyzer SHALL measure wall thickness at multiple sample points across all surfaces
2. THE Geometry_Analyzer SHALL use ray casting from surface points to detect opposing surfaces
3. THE Geometry_Analyzer SHALL calculate the minimum distance between opposing surfaces as wall thickness
4. THE Geometry_Analyzer SHALL sample at least 1000 points per square meter of surface area
5. WHEN wall thickness is measured, THE Geometry_Analyzer SHALL record the 3D coordinates of the thinnest location
6. THE Geometry_Analyzer SHALL measure wall thickness with ±0.01mm accuracy
7. WHEN multiple thin wall locations exist, THE Geometry_Analyzer SHALL identify all locations below the threshold
8. THE Geometry_Analyzer SHALL distinguish between intentional thin features (ribs, fins) and structural walls
9. IF opposing surfaces cannot be detected, THEN THE Geometry_Analyzer SHALL report the feature as a non-wall element

### Requirement 3: Corner Radius Detection and Measurement

**User Story:** As a DFM engineer, I want the system to detect and measure corner radii accurately, so that sharp corner violations are identified with precise measurements.

#### Acceptance Criteria

1. WHEN a 3D mesh is analyzed, THE Feature_Detector SHALL identify all internal corners
2. WHEN a 3D mesh is analyzed, THE Feature_Detector SHALL identify all external corners
3. WHEN a corner is detected, THE Geometry_Analyzer SHALL measure the radius of curvature
4. THE Geometry_Analyzer SHALL measure corner radii with ±0.01mm accuracy
5. WHEN a corner radius is below 0.5mm, THE Feature_Detector SHALL classify it as a sharp corner
6. THE Feature_Detector SHALL record the 3D coordinates of each detected corner
7. THE Feature_Detector SHALL distinguish between fillets (rounded transitions) and chamfers (beveled transitions)
8. WHEN a chamfer is detected, THE Geometry_Analyzer SHALL measure the chamfer distance
9. THE Feature_Detector SHALL detect corners at edges where surface normals change by more than 45 degrees

### Requirement 4: Hole Detection and Measurement

**User Story:** As a DFM engineer, I want the system to detect all holes and measure their specifications accurately, so that hole-related DFM issues are identified with correct dimensions.

#### Acceptance Criteria

1. WHEN a 3D mesh is analyzed, THE Feature_Detector SHALL identify all cylindrical holes
2. WHEN a hole is detected, THE Geometry_Analyzer SHALL measure the hole diameter
3. WHEN a hole is detected, THE Geometry_Analyzer SHALL measure the hole depth
4. WHEN a hole is detected, THE Geometry_Analyzer SHALL determine if the hole is through or blind
5. THE Geometry_Analyzer SHALL measure hole dimensions with ±0.01mm accuracy
6. THE Feature_Detector SHALL record the 3D coordinates of each hole center point
7. THE Feature_Detector SHALL record the axis direction vector for each hole
8. WHEN multiple holes exist, THE Geometry_Analyzer SHALL measure the spacing between hole centers
9. THE Feature_Detector SHALL detect threaded holes by identifying helical surface patterns
10. WHEN a threaded hole is detected, THE Geometry_Analyzer SHALL determine the thread pitch and diameter

### Requirement 5: Pocket Detection and Measurement

**User Story:** As a DFM engineer, I want the system to detect pockets and measure their dimensions, so that deep pocket violations and small pocket issues are identified accurately.

#### Acceptance Criteria

1. WHEN a 3D mesh is analyzed, THE Feature_Detector SHALL identify all pocket features
2. WHEN a pocket is detected, THE Geometry_Analyzer SHALL measure the pocket depth
3. WHEN a pocket is detected, THE Geometry_Analyzer SHALL measure the pocket width and length
4. WHEN a pocket is detected, THE Geometry_Analyzer SHALL measure the corner radii at the pocket bottom
5. THE Geometry_Analyzer SHALL measure pocket dimensions with ±0.01mm accuracy
6. THE Feature_Detector SHALL record the 3D coordinates of the pocket center
7. THE Feature_Detector SHALL distinguish between open pockets and closed pockets
8. WHEN a pocket depth exceeds 3 times the pocket width, THE Feature_Detector SHALL classify it as a deep pocket
9. THE Geometry_Analyzer SHALL measure the wall thickness around pocket perimeters

### Requirement 6: Boss and Rib Detection

**User Story:** As a DFM engineer, I want the system to detect bosses and ribs and measure their dimensions, so that manufacturability issues with these features are identified.

#### Acceptance Criteria

1. WHEN a 3D mesh is analyzed, THE Feature_Detector SHALL identify all boss features (raised cylindrical protrusions)
2. WHEN a 3D mesh is analyzed, THE Feature_Detector SHALL identify all rib features (thin wall protrusions)
3. WHEN a boss is detected, THE Geometry_Analyzer SHALL measure the boss height
4. WHEN a boss is detected, THE Geometry_Analyzer SHALL measure the boss diameter
5. WHEN a rib is detected, THE Geometry_Analyzer SHALL measure the rib thickness
6. WHEN a rib is detected, THE Geometry_Analyzer SHALL measure the rib height
7. THE Geometry_Analyzer SHALL measure boss and rib dimensions with ±0.01mm accuracy
8. THE Feature_Detector SHALL record the 3D coordinates of each boss and rib location
9. WHEN a rib height exceeds 3 times the rib thickness, THE Feature_Detector SHALL classify it as a tall rib

### Requirement 7: Feature Spacing Measurement

**User Story:** As a DFM engineer, I want the system to measure spacing between features, so that insufficient spacing violations are detected.

#### Acceptance Criteria

1. WHEN multiple features are detected, THE Geometry_Analyzer SHALL measure the minimum distance between feature edges
2. THE Geometry_Analyzer SHALL measure feature spacing with ±0.01mm accuracy
3. WHEN two holes are detected, THE Geometry_Analyzer SHALL measure center-to-center spacing
4. WHEN a hole is near an edge, THE Geometry_Analyzer SHALL measure the distance from hole center to nearest edge
5. WHEN features are closer than 2 times the feature size, THE Geometry_Analyzer SHALL flag potential spacing issues
6. THE Geometry_Analyzer SHALL measure spacing in 3D space accounting for non-planar surfaces

### Requirement 8: DFM Rule Validation with Accurate Measurements

**User Story:** As a DFM engineer, I want all DFM rules to be checked using accurate measurements, so that reported violations reflect real geometry issues.

#### Acceptance Criteria

1. WHEN features are detected and measured, THE DFM_Rule_Engine SHALL check each feature against manufacturing rules
2. THE DFM_Rule_Engine SHALL use measured values (not estimated values) for all rule checks
3. WHEN a feature violates a manufacturing rule, THE DFM_Rule_Engine SHALL record the measured value and the rule threshold
4. THE DFM_Rule_Engine SHALL record the 3D coordinates of each violation location
5. WHEN a wall thickness violation is detected, THE DFM_Rule_Engine SHALL include the measured thickness and minimum required thickness
6. WHEN a corner radius violation is detected, THE DFM_Rule_Engine SHALL include the measured radius and minimum required radius
7. WHEN a hole dimension violation is detected, THE DFM_Rule_Engine SHALL include the measured dimension and the rule constraint
8. THE DFM_Rule_Engine SHALL check rules specific to the selected manufacturing process (CNC, Sheet Metal, Injection Molding, Die Casting, Welding)
9. THE DFM_Rule_Engine SHALL check rules specific to the selected material

### Requirement 9: 3D Visualization with Highlighted Thin Walls

**User Story:** As a DFM engineer, I want to see 3D renderings with thin walls highlighted in red, so that I can visually identify where wall thickness violations occur.

#### Acceptance Criteria

1. WHEN thin wall violations are detected, THE Visualization_Engine SHALL generate a 3D rendering of the part
2. THE Visualization_Engine SHALL highlight all thin wall locations in red color
3. THE Visualization_Engine SHALL use the actual 3D mesh geometry for rendering
4. THE Visualization_Engine SHALL apply red highlighting to mesh faces at violation coordinates
5. THE Visualization_Engine SHALL render non-violation areas in neutral gray color
6. THE Visualization_Engine SHALL generate renderings at minimum 1920x1080 resolution
7. THE Visualization_Engine SHALL include axis indicators and scale reference in renderings
8. WHEN multiple thin wall locations exist, THE Visualization_Engine SHALL highlight all violation locations in the same rendering

### Requirement 10: 3D Visualization with Highlighted Sharp Corners

**User Story:** As a DFM engineer, I want to see 3D renderings with sharp corners highlighted in red, so that I can visually identify where corner radius violations occur.

#### Acceptance Criteria

1. WHEN sharp corner violations are detected, THE Visualization_Engine SHALL generate a 3D rendering of the part
2. THE Visualization_Engine SHALL highlight all sharp corner locations in red color
3. THE Visualization_Engine SHALL apply red highlighting to mesh faces adjacent to sharp corners
4. THE Visualization_Engine SHALL create a visible red marker at each sharp corner coordinate
5. WHEN multiple sharp corners exist, THE Visualization_Engine SHALL highlight all violation locations in the same rendering

### Requirement 11: 3D Visualization with Highlighted Hole Violations

**User Story:** As a DFM engineer, I want to see 3D renderings with problematic holes highlighted in red, so that I can visually identify where hole-related violations occur.

#### Acceptance Criteria

1. WHEN hole dimension violations are detected, THE Visualization_Engine SHALL generate a 3D rendering of the part
2. THE Visualization_Engine SHALL highlight all problematic hole surfaces in red color
3. THE Visualization_Engine SHALL apply red highlighting to the cylindrical surfaces of violating holes
4. WHEN a hole is too small, THE Visualization_Engine SHALL highlight the entire hole surface in red
5. WHEN holes are too close together, THE Visualization_Engine SHALL highlight both holes in red
6. WHEN a hole is too close to an edge, THE Visualization_Engine SHALL highlight the hole and adjacent edge in red

### Requirement 12: 3D Visualization with Highlighted Deep Pockets

**User Story:** As a DFM engineer, I want to see 3D renderings with deep pockets highlighted in red, so that I can visually identify where pocket depth violations occur.

#### Acceptance Criteria

1. WHEN deep pocket violations are detected, THE Visualization_Engine SHALL generate a 3D rendering of the part
2. THE Visualization_Engine SHALL highlight all deep pocket surfaces in red color
3. THE Visualization_Engine SHALL apply red highlighting to pocket bottom and wall surfaces
4. THE Visualization_Engine SHALL use shading to emphasize pocket depth in renderings
5. WHEN multiple deep pockets exist, THE Visualization_Engine SHALL highlight all violation locations in the same rendering

### Requirement 13: Multi-View 3D Rendering

**User Story:** As a DFM engineer, I want to see multiple views of the part with highlighted violations, so that I can understand the spatial context of each issue.

#### Acceptance Criteria

1. WHEN DFM violations are detected, THE Visualization_Engine SHALL generate renderings from multiple viewing angles
2. THE Visualization_Engine SHALL generate front, top, and isometric views
3. THE Visualization_Engine SHALL maintain consistent highlighting across all views
4. THE Visualization_Engine SHALL automatically select the best viewing angle to show each violation
5. WHEN a violation is not visible from standard views, THE Visualization_Engine SHALL generate an additional custom view showing the violation

### Requirement 14: Comprehensive Feature Report

**User Story:** As a DFM engineer, I want a detailed report of all detected features with measurements, so that I can review the complete geometric analysis.

#### Acceptance Criteria

1. WHEN geometry analysis completes, THE Geometry_Analyzer SHALL generate a feature report
2. THE feature report SHALL list all detected walls with thickness measurements and coordinates
3. THE feature report SHALL list all detected corners with radius measurements and coordinates
4. THE feature report SHALL list all detected holes with diameter, depth, and coordinates
5. THE feature report SHALL list all detected pockets with dimensions and coordinates
6. THE feature report SHALL list all detected bosses and ribs with dimensions and coordinates
7. THE feature report SHALL include measurement units (millimeters) for all dimensions
8. THE feature report SHALL include confidence scores for feature detection (0-100%)
9. THE feature report SHALL be exportable in JSON format

### Requirement 15: Integration with Existing DFM Analysis

**User Story:** As a DFM engineer, I want the enhanced geometry analysis to integrate seamlessly with existing DFM analyzers, so that all manufacturing processes benefit from accurate measurements.

#### Acceptance Criteria

1. WHEN geometry analysis completes, THE Geometry_Analyzer SHALL provide measurement data to all process analyzers
2. THE Geometry_Analyzer SHALL provide data in the same format as the current simple_cad_parser
3. THE Geometry_Analyzer SHALL replace estimated measurements with actual measurements in the analysis dictionary
4. THE Geometry_Analyzer SHALL maintain backward compatibility with existing analyzer interfaces
5. WHEN a process analyzer requests wall thickness, THE Geometry_Analyzer SHALL provide measured wall thickness (not estimated)
6. WHEN a process analyzer requests hole data, THE Geometry_Analyzer SHALL provide complete hole specifications
7. THE Geometry_Analyzer SHALL provide feature coordinates for all detected features to enable visualization

### Requirement 16: Performance Requirements

**User Story:** As a DFM engineer, I want geometry analysis to complete in reasonable time, so that I can analyze parts efficiently.

#### Acceptance Criteria

1. WHEN a STEP file under 10MB is analyzed, THE Geometry_Analyzer SHALL complete analysis within 30 seconds
2. WHEN a STEP file between 10MB and 50MB is analyzed, THE Geometry_Analyzer SHALL complete analysis within 2 minutes
3. THE Geometry_Analyzer SHALL provide progress updates during analysis
4. THE Visualization_Engine SHALL generate each 3D rendering within 10 seconds
5. WHEN analysis is in progress, THE system SHALL remain responsive to user interface interactions

### Requirement 17: Error Handling and Validation

**User Story:** As a DFM engineer, I want clear error messages when geometry analysis fails, so that I can understand what went wrong and take corrective action.

#### Acceptance Criteria

1. IF STEP file parsing fails, THEN THE STEP_Parser SHALL provide an error message identifying the specific parsing issue
2. IF mesh generation fails, THEN THE Geometry_Analyzer SHALL provide an error message and attempt fallback analysis
3. IF feature detection fails for a specific feature type, THEN THE Feature_Detector SHALL log the failure and continue with other feature types
4. IF measurement accuracy cannot be guaranteed, THEN THE Geometry_Analyzer SHALL include a warning in the feature report
5. WHEN geometry is non-manifold or has defects, THE Geometry_Analyzer SHALL report the defects and attempt analysis on valid portions
6. IF visualization generation fails, THEN THE Visualization_Engine SHALL provide an error message and generate a basic rendering without highlights

### Requirement 18: Measurement Validation

**User Story:** As a DFM engineer, I want confidence that measurements are accurate, so that I can trust the DFM analysis results.

#### Acceptance Criteria

1. WHEN geometry is analyzed, THE Geometry_Analyzer SHALL validate measurements against known geometric constraints
2. THE Geometry_Analyzer SHALL verify that measured wall thickness is less than or equal to part dimensions
3. THE Geometry_Analyzer SHALL verify that hole diameters are positive values
4. THE Geometry_Analyzer SHALL verify that pocket depths are less than part height
5. WHEN measurements fail validation, THE Geometry_Analyzer SHALL flag the measurement as potentially inaccurate
6. THE Geometry_Analyzer SHALL compare measurements from multiple analysis methods when available
7. WHEN measurements from different methods disagree by more than 0.1mm, THE Geometry_Analyzer SHALL report the discrepancy

### Requirement 19: Mesh Quality Analysis

**User Story:** As a DFM engineer, I want to know if the 3D mesh quality affects measurement accuracy, so that I can assess confidence in the results.

#### Acceptance Criteria

1. WHEN a mesh is loaded, THE Mesh_Analyzer SHALL evaluate mesh quality metrics
2. THE Mesh_Analyzer SHALL check if the mesh is watertight (closed volume)
3. THE Mesh_Analyzer SHALL check for degenerate triangles (zero area)
4. THE Mesh_Analyzer SHALL check for non-manifold edges
5. THE Mesh_Analyzer SHALL calculate average triangle quality
6. WHEN mesh quality is poor, THE Mesh_Analyzer SHALL include a warning in the analysis report
7. THE Mesh_Analyzer SHALL report the number of vertices and faces in the mesh
8. WHEN mesh has defects, THE Mesh_Analyzer SHALL attempt automatic repair before analysis

### Requirement 20: Configuration and Customization

**User Story:** As a DFM engineer, I want to configure analysis parameters, so that I can adjust sensitivity and performance for different use cases.

#### Acceptance Criteria

1. THE Geometry_Analyzer SHALL support configuration of sampling density for wall thickness measurement
2. THE Geometry_Analyzer SHALL support configuration of minimum feature size threshold
3. THE Geometry_Analyzer SHALL support configuration of measurement tolerance
4. THE Feature_Detector SHALL support configuration of corner angle threshold for sharp corner detection
5. THE Visualization_Engine SHALL support configuration of highlight color
6. THE Visualization_Engine SHALL support configuration of rendering resolution
7. WHERE custom configuration is provided, THE system SHALL use custom values instead of defaults
8. WHERE custom configuration is not provided, THE system SHALL use default values optimized for typical DFM analysis

