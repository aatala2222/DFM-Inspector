"# Reference Documents Summary" 
"" 
"## Source: reference_pdfs/ folder" 
"" 
"?? NOTE: The agent cannot read PDFs directly." 
"Key content from each PDF should be extracted below." 
"" 
"## Available Reference Documents" 
"" 
"- $(basename "$file")" 
"" 
"## Extracted Content" 
"" 
"TODO: Paste key content from each PDF below." 

COMPREHENSIVE
DESIGN FOR MANUFACTURABILITY
GUIDELINES

CNC Machining Process
3-Axis  |  4-Axis  |  5-Axis Milling  |  CNC Turning  |  Secondary Operations

For Product Designers & Engineers
Document Version 1.0  |  March 2026
 
Table of Contents
Table of Contents	2
1. Introduction and Purpose	4
1.1 How to Use This Document	4
1.2 Units and Conventions	4
2. General Design Principles	5
2.1 Fundamental DFM Rules	5
2.2 Cost Drivers in CNC Machining	5
3. Material Selection Guidelines	7
3.1 Metal Machinability Reference	7
3.2 Plastics Machinability Reference	8
4. Feature-Specific Design Guidelines	9
4.1 Holes	9
4.1.1 Through Holes	9
4.1.2 Blind Holes	9
4.1.3 Threaded Holes	10
4.2 Walls and Thin Features	11
4.3 Pockets and Cavities	11
4.3.1 Internal Corner Radius Selection Guide	12
4.4 Fillets and Radii	13
4.5 Chamfers	13
4.6 Threads (External and Internal)	15
4.6.1 Preferred Standard Thread Sizes	15
4.6.2 Thread Design Rules	15
4.7 Undercuts and Internal Features	15
4.8 Surface Finish	17
4.9 Slots and Grooves	17
5. Tolerancing Guidelines	19
5.1 General Tolerance Classes	19
5.2 Geometric Dimensioning & Tolerancing (GD&T)	19
6. 3-Axis Milling Guidelines	21
6.1 Design Constraints	21
6.2 Recommended Envelope and Capacity	21
7. 4-Axis Milling Guidelines	22
7.1 When to Design for 4-Axis	22
7.2 Design Rules for 4-Axis	22
8. 5-Axis Milling Guidelines	23
8.1 Advantages of 5-Axis Machining	23
8.2 Design Rules for 5-Axis	23
9. CNC Turning Guidelines	24
9.1 General Turning Design Rules	24
9.2 Turning Feature Design	24
9.3 Swiss-Type Turning	25
10. Workholding Considerations	26
10.1 Design-for-Fixturing Rules	26
11. Secondary Operations	27
11.1 Heat Treatment	27
11.2 Surface Treatments and Coatings	27
11.3 Grinding	28
11.4 EDM (Electrical Discharge Machining)	29
11.5 Deburring	29
12. Common DFM Violations Checklist	31
13. Cost Optimization Strategies	32
13.1 Design-Level Strategies	32
13.2 Material-Level Strategies	32
14. Drawing and Documentation Best Practices	33
14.1 Required Drawing Information	33
15. Reference Tables	34
15.1 Standard Metric Drill Sizes	34
15.2 Tap Drill Sizes (Metric Coarse Threads, ~75% Thread)	34
15.3 Standard End Mill Diameters	34
15.4 Unit Conversion Quick Reference	34
Appendix A: DFM Review Workflow	36
Appendix B: Glossary of CNC Machining Terms	37

 
 
1. Introduction and Purpose
This document provides comprehensive Design for Manufacturability (DFM) guidelines for CNC machining processes. It serves as a definitive reference for product designers and engineers to ensure that part designs are optimized for manufacturing efficiency, cost-effectiveness, and quality. These guidelines apply across the full spectrum of CNC operations including 3-axis, 4-axis, and 5-axis milling, CNC turning (standard and Swiss-type), as well as all common secondary operations such as heat treatment, surface finishing, and coatings.
Following these guidelines will help reduce manufacturing lead times, minimize tooling costs, improve part quality, reduce scrap rates, and ensure consistent repeatability across production runs.
1.1 How to Use This Document
Each section contains specific design rules organized by feature type or process. Recommended values represent standard best practice; achievable values represent what is possible with specialized tooling or setup, usually at higher cost. Designers should target recommended values wherever possible and consult with manufacturing engineering before specifying achievable limits.
1.2 Units and Conventions
Unless otherwise noted, all dimensions are in millimeters (mm). Tolerances are bilateral unless shown otherwise. Angles are in degrees. Surface roughness is expressed as Ra in micrometers. Where imperial equivalents are helpful, they are shown in parentheses.
2. General Design Principles
2.1 Fundamental DFM Rules
•	Minimize the number of setups: Design parts so they can be machined in as few orientations as possible. Each additional setup adds cost, time, and potential tolerance stack-up.
•	Design for standard tooling: Use standard drill sizes, standard thread sizes, and standard fillet radii that correspond to common tool diameters. Avoid features that require custom tooling.
•	Avoid unnecessary tight tolerances: Specify only the tolerances that are functionally necessary. Tighter tolerances exponentially increase machining time and inspection costs.
•	Ensure tool access: Every feature must be reachable by a cutting tool. Consider tool length, diameter, and approach angle when designing internal features.
•	Minimize material removal: Design near-net-shape parts where possible. Excessive material removal wastes material, increases cycle time, and accelerates tool wear.
•	Design for workholding: Ensure the part has adequate surfaces for clamping or fixturing. Include datum surfaces that can be reliably referenced across setups.
•	Use uniform wall thicknesses: Uniform walls reduce the risk of distortion during machining and heat treatment. Gradual transitions are preferred over abrupt changes.
•	Add fillets to internal corners: All internal corners require a fillet radius at minimum equal to the tool radius. Sharp 90-degree internal corners are physically impossible with rotary cutters.
2.2 Cost Drivers in CNC Machining
Understanding the primary cost drivers helps designers make informed trade-off decisions during the design process. The following table ranks common cost drivers from highest to lowest impact.
Rank	Cost Driver	Impact	Design Mitigation
1	Number of setups	Very High	Design for single-setup machining; add fixture-friendly features
2	Tight tolerances (<0.025 mm)	Very High	Apply tight tolerances only to functional mating surfaces
3	Deep pockets / cavities	High	Limit depth-to-width ratio to 4:1 or less
4	Thin walls	High	Maintain minimum 0.8 mm (metals) or 1.5 mm (plastics)
5	Non-standard tooling	High	Use standard drill/end mill sizes and thread pitches
6	Complex surface finishes	Medium-High	Specify surface finish only where functionally required
7	Small internal radii	Medium	Use radii that match standard tool diameters (R1.5, R3, R6 mm)
8	Deep holes	Medium	Keep depth-to-diameter ratio below 10:1 where possible
9	Material hardness	Medium	Consider pre-hardened stock to avoid post-machining heat treatment
10	Part size / weight	Low-Medium	Design within standard machine envelopes

3. Material Selection Guidelines
Material selection profoundly affects machinability, cost, tool life, achievable tolerances, and surface finish. The following table provides machinability guidance for common engineering materials.
3.1 Metal Machinability Reference
Material	Machinability Rating	Typical Ra (um)	Notes
Aluminum 6061-T6	Excellent	0.4 - 1.6	Preferred general-purpose alloy; excellent chip formation
Aluminum 7075-T6	Excellent	0.4 - 1.6	Higher strength; slightly more tool wear than 6061
Aluminum 2024-T3	Good - Excellent	0.8 - 1.6	Gummy when annealed; machine in tempered condition
Brass C360	Excellent	0.4 - 0.8	Free-machining; ideal for high-volume turned parts
Carbon Steel 1018	Good	0.8 - 3.2	Low cost; good for general structural parts
Carbon Steel 1045	Good	1.6 - 3.2	Medium carbon; hardenable; moderate tool wear
Alloy Steel 4140	Fair - Good	1.6 - 3.2	Pre-hardened grades (28-32 HRC) available; common structural
Alloy Steel 4340	Fair	1.6 - 6.3	High strength; requires carbide or ceramic tooling
Stainless Steel 303	Good	0.8 - 3.2	Free-machining SS; preferred when corrosion resistance needed
Stainless Steel 304	Fair	1.6 - 3.2	Work-hardens rapidly; use sharp tools, constant feed
Stainless Steel 316	Fair	1.6 - 6.3	More difficult than 304; gummy chips; superior corrosion resistance
Stainless Steel 17-4 PH	Fair	1.6 - 3.2	Machine in Condition A; heat treat after; precipitation hardening
Titanium Ti-6Al-4V	Poor - Fair	1.6 - 6.3	Low thermal conductivity; requires rigid setup, flood coolant
Inconel 718	Poor	3.2 - 6.3	Extreme tool wear; use ceramic inserts; low speeds
Copper C110	Good	0.4 - 1.6	Soft; burrs easily; excellent thermal/electrical conductivity
Tool Steel D2	Poor	3.2 - 6.3	Very hard (58-62 HRC); EDM often preferred for complex shapes
Tool Steel A2	Fair	1.6 - 3.2	Air-hardening; machine in annealed state then heat treat

3.2 Plastics Machinability Reference
Material	Machinability	Typical Ra (um)	Notes
Delrin (POM / Acetal)	Excellent	0.4 - 1.6	Best overall plastic for CNC; excellent dimensional stability
Nylon 6/6	Good	0.8 - 3.2	Absorbs moisture; may swell; dry before machining for best results
PEEK	Good	0.8 - 1.6	High cost; excellent for high-temp applications; carbide tools recommended
Polycarbonate (PC)	Good	0.8 - 1.6	Transparent; stress-cracks with some coolants; use air blast
Acrylic (PMMA)	Good	0.2 - 0.8	Brittle; cracks if clamped too tightly; excellent optical clarity
UHMW-PE	Fair	1.6 - 3.2	Very flexible; deflects under tool pressure; use sharp tools
PTFE (Teflon)	Fair	1.6 - 6.3	Deforms under clamping; cold creep; vacuum fixturing often needed
ABS	Good	0.8 - 3.2	Easy to machine; melts at high speeds; use moderate RPM
PEI (Ultem)	Good	0.8 - 1.6	Amorphous; good dimensional stability; aerospace applications
Garolite G-10/FR4	Fair	3.2 - 6.3	Abrasive fiberglass; rapid tool wear; diamond-coated tools preferred

Material Selection Tip
When in doubt, Aluminum 6061-T6 offers the best combination of machinability, strength, corrosion resistance, and cost for prototyping and general-purpose applications. For plastic prototypes, Delrin (Acetal/POM) is the gold standard for CNC machining due to its excellent dimensional stability and chip formation.

4. Feature-Specific Design Guidelines
This section provides detailed design rules for each common CNC-machined feature type. Each subsection includes recommended values, achievable limits, and the rationale behind each guideline.
4.1 Holes
Holes are among the most common features in CNC machined parts. Proper hole design significantly affects cycle time, tool life, and achievable quality.
4.1.1 Through Holes
Parameter	Recommended	Achievable	Notes
Minimum diameter	1.0 mm (0.040")	0.5 mm (0.020")	Smaller diameters require specialized micro-drills
Maximum depth-to-diameter ratio	6:1	10:1	Beyond 6:1 requires peck drilling; beyond 10:1 consider gun drilling
Preferred diameters	Standard drill sizes	Any	Use standard fractional, letter, or metric drill sizes to avoid reaming
Diameter tolerance (standard)	+/- 0.05 mm	+/- 0.013 mm	Tighter tolerance requires reaming or boring
Diameter tolerance (reamed)	+/- 0.013 mm	+/- 0.005 mm	H7 tolerance class achievable with reaming
Position tolerance	+/- 0.05 mm	+/- 0.013 mm	Tighter requires precision boring or jig boring
Edge distance (min)	Diameter x 1.5	Diameter x 1.0	Less than 1x diameter risks breakout and deformation
Hole-to-hole spacing (min)	Diameter x 2.0	Diameter x 1.5	Closer spacing risks thin wall deflection between holes
Entry/exit surface	Perpendicular	Up to 5 deg	Angled surfaces cause drill walk; use spot drill or flat

4.1.2 Blind Holes
Parameter	Recommended	Achievable	Notes
Bottom geometry	118 deg cone (drill point)	Flat bottom	Flat bottom requires end mill; adds cost and time
Depth tolerance	+/- 0.13 mm	+/- 0.05 mm	Measured to full diameter, not drill point
Max depth-to-diameter	4:1	8:1	Chip evacuation is harder in blind holes
Minimum corner radius at bottom	0.5 x diameter	0.1 mm	Flat bottom requires separate end mill operation
Minimum remaining wall thickness	0.5 mm	0.3 mm	Thin floors prone to deflection and breakthrough

Design Tip – Holes
Wherever possible, design through holes instead of blind holes. Through holes are faster to machine, easier to deburr, easier to inspect, and produce better surface finishes. If a blind hole is functionally required, accept the standard 118-degree drill-point bottom unless a flat bottom is absolutely necessary.

4.1.3 Threaded Holes
Parameter	Recommended	Achievable	Notes
Minimum thread size	M3 / #4-40	M1.6 / #0-80	Smaller threads are fragile and limit torque capacity
Thread engagement depth	1.5 x diameter	3.0 x diameter	Beyond 2x adds minimal strength; increases tap breakage risk
Thread relief at bottom	1-2 pitches clearance	0.5 pitch	Relief prevents tap bottoming and breakage
Preferred thread form	Standard metric or UNC/UNF	Custom	Standard threads use stock taps; custom requires thread milling
Thread class (metric)	6H	4H	Tighter classes require thread milling or precision tapping
Thread class (imperial)	2B	3B	3B requires controlled-lead tapping or thread milling
Minimum wall to thread	2.0 x pitch	1.0 x pitch	Thin walls deform under tapping forces
Chamfer at thread entry	0.5 mm x 45 deg	0.25 mm x 45 deg	Chamfer guides the fastener and protects thread start

4.2 Walls and Thin Features
Thin walls are one of the most common causes of machining problems. Inadequate wall thickness leads to vibration (chatter), deflection, distortion, and in extreme cases, part failure during machining.
Material Category	Min Wall (Recommended)	Min Wall (Achievable)	Max Unsupported Height-to-Thickness Ratio
Aluminum alloys	0.8 mm (0.031")	0.5 mm (0.020")	15:1
Carbon & alloy steels	0.8 mm (0.031")	0.5 mm (0.020")	12:1
Stainless steels	1.0 mm (0.040")	0.5 mm (0.020")	10:1
Titanium alloys	1.0 mm (0.040")	0.6 mm (0.024")	8:1
Copper alloys (soft)	1.0 mm (0.040")	0.5 mm (0.020")	10:1
Engineering plastics	1.5 mm (0.060")	0.8 mm (0.031")	20:1
Soft plastics (PE, PTFE)	2.0 mm (0.079")	1.0 mm (0.040")	12:1

Critical Warning – Thin Walls
Thin walls adjacent to deep pockets are the single most common DFM violation. The combination of thin wall + deep pocket creates a lever arm that amplifies vibration. If thin walls are unavoidable, use light cuts with high spindle speeds, add temporary support ribs that are removed in a final pass, or consider stress-relief heat treatment between roughing and finishing operations.

4.3 Pockets and Cavities
Pockets are enclosed material-removal features. Their design directly impacts tool selection, cycle time, and achievable quality.
Parameter	Recommended	Achievable	Notes
Min internal corner radius	1/3 of pocket depth	Tool radius + 0.1 mm	Must match or exceed end mill radius; include 0.1 mm clearance
Max depth-to-width ratio	4:1	6:1	Deep narrow pockets require long-reach tools that deflect
Min pocket width	2.0 x tool diameter	1.0 x tool diameter	Narrow pockets limit chip evacuation and tool engagement
Floor flatness	0.05 mm over 50 mm	0.013 mm over 50 mm	Depends on tool deflection and machine rigidity
Floor-to-wall transition	Fillet = tool radius	0.5 mm min	Sharp corners impossible; design fillet to match standard tool
Pocket bottom thickness	Min 1.0 mm (metal)	0.5 mm (metal)	Thin bottoms deflect and risk breakthrough
Draft angle on walls	0 deg (vertical)	0 deg (vertical)	CNC can cut vertical walls; draft not needed unlike injection molding
Step-down transitions	Fillet R 0.5 mm min	R 0.25 mm	Smooth transitions reduce stress concentration and tool loading

4.3.1 Internal Corner Radius Selection Guide
The internal corner radius is one of the most critical dimensions in pocket design. It determines the minimum tool diameter, which in turn affects achievable depth and surface finish. Use the following guide to select appropriate corner radii.
Pocket Depth	Minimum Corner Radius	Standard Tool Diameter	Tool L/D Ratio
Up to 6 mm	R 1.5 mm	3 mm end mill	2:1
Up to 12 mm	R 3.0 mm	6 mm end mill	2:1
Up to 25 mm	R 5.0 mm	10 mm end mill	2.5:1
Up to 38 mm	R 6.0 mm	12 mm end mill	3.2:1
Up to 50 mm	R 8.0 mm	16 mm end mill	3.1:1
Up to 75 mm	R 10.0 mm	20 mm end mill	3.75:1
Up to 100 mm	R 12.0 mm	25 mm end mill	4:1

Internal Corner Radius Tip
Always specify the internal corner radius as slightly larger than the tool radius (at least 0.1 mm or 10% larger). This prevents the tool from engaging the full 180 degrees of its circumference in corners, which causes tool deflection, chatter, and premature wear. For example, if using a 6 mm end mill (R3), specify R3.5 mm on the drawing.

4.4 Fillets and Radii
Fillets and radii are critical for both manufacturability and structural integrity. Internal fillets are limited by tool geometry, while external radii offer more design freedom.
Feature Type	Recommended Radius	Minimum Achievable	Notes
Internal vertical fillets	R 3.0 mm	R 0.25 mm	Must match cutter radius; controls minimum tool size
Internal floor fillets	R 1.0 mm	R 0.25 mm	Ball end mill radius; affects pocket-floor transition
External edges	R 0.5 mm (chamfer preferred)	Sharp (burr removed)	Sharp external edges are achievable but fragile
Fillet between ribs and walls	R 1.0 mm	R 0.5 mm	Reduces stress concentration at junctions
Undercut fillets	R 1.0 mm	R 0.5 mm	Requires T-slot cutter or special form tool
Blend radius between surfaces	R 3.0 mm or greater	R 0.5 mm	Larger radii allow faster feed rates and better finish

Consistency Tip
Use a maximum of 2-3 different fillet radii throughout a part. This minimizes tool changes and keeps cycle times low. Pick standard radii that correspond to common tool diameters: R1.5, R3.0, R5.0, R6.0, R8.0, R10.0, and R12.0 mm.

4.5 Chamfers
Chamfers are preferred over fillets for external edges because they can be cut quickly with a standard chamfer mill in a single pass. They also ease assembly, remove burrs, and reduce stress concentrations on external edges.
Parameter	Recommended	Achievable	Notes
Standard chamfer angle	45 degrees	Any angle	45 deg is default; other angles require angle-specific tools
Minimum chamfer size	0.25 mm x 45 deg	0.1 mm x 45 deg	Very small chamfers hard to inspect and maintain consistency
Maximum chamfer size	3.0 mm x 45 deg	Limited by geometry	Large chamfers may require multiple passes
Chamfer on hole entry	0.5 mm x 45 deg	0.25 mm x 45 deg	Aids fastener insertion and deburrs hole edge
Chamfer tolerance	+/- 0.25 mm	+/- 0.1 mm	Chamfer size is difficult to measure precisely

4.6 Threads (External and Internal)
Thread design affects both the machining process and the functionality of the final assembly. Use standard thread sizes whenever possible to leverage off-the-shelf taps, dies, and thread mills.
4.6.1 Preferred Standard Thread Sizes
Metric (Coarse)	Metric (Fine)	Imperial (UNC)	Imperial (UNF)
M3 x 0.5	M3 x 0.35	#4-40	#4-48
M4 x 0.7	M4 x 0.5	#6-32	#6-40
M5 x 0.8	M5 x 0.5	#8-32	#8-36
M6 x 1.0	M6 x 0.75	#10-24	#10-32
M8 x 1.25	M8 x 1.0	1/4-20	1/4-28
M10 x 1.5	M10 x 1.25	5/16-18	5/16-24
M12 x 1.75	M12 x 1.25	3/8-16	3/8-24
M16 x 2.0	M16 x 1.5	1/2-13	1/2-20
M20 x 2.5	M20 x 1.5	5/8-11	5/8-18
M24 x 3.0	M24 x 2.0	3/4-10	3/4-16

4.6.2 Thread Design Rules
•	Use coarse threads as default: Coarse threads are stronger, more forgiving of tolerance variation, and less prone to cross-threading. Use fine threads only when vibration resistance or fine adjustment is needed.
•	Thread engagement depth: 1.5x to 2.0x the nominal thread diameter provides full strength in steel and aluminum. Beyond 2.0x adds negligible strength but increases tap breakage risk.
•	Thread relief: Allow at least 1.5 to 2 pitches of unthreaded depth at the bottom of blind tapped holes for chip clearance and to prevent tap bottoming.
•	Thread milling vs tapping: Thread milling is preferred for large threads (> M12), hard materials (> 35 HRC), blind holes with limited depth, and when thread quality is critical. Tapping is faster and preferred for smaller threads in softer materials.
•	Minimum wall around threads: Maintain at least 2x the thread pitch between the thread major diameter and any adjacent wall or feature.

4.7 Undercuts and Internal Features
Undercuts are features that cannot be reached by a standard end mill approaching from directly above. They require specialized tooling (T-slot cutters, lollipop cutters, or keyway cutters) and add significant cost and complexity.
Parameter	Recommended	Achievable	Notes
Avoid undercuts if possible	Yes	N/A	Redesign to eliminate undercuts wherever possible
Standard O-ring groove width	Per O-ring spec	Per spec	Use standard AS568 groove dimensions
T-slot width	Standard T-slot sizes	Custom	Standard T-slots match standard T-slot cutters
Undercut depth	< 2x tool neck diameter	3x tool neck	Deep undercuts require long slender tools that deflect
Min access opening	Tool diameter + 2 mm	Tool diameter + 0.5 mm	Tool must pass through opening to reach undercut
Dovetail angle	45 or 60 degrees	Any standard angle	Match standard dovetail cutter angles

DFM Recommendation
If an undercut is required for an O-ring groove, retaining ring groove, or similar functional feature, specify it with standard dimensions that match commercially available cutters. Custom undercut profiles are expensive and have long lead times for tooling. Wherever possible, redesign the part so undercut features become accessible from a standard tool direction.

4.8 Surface Finish
Surface finish is specified as Ra (arithmetic average roughness) in micrometers. The achievable finish depends on the material, tool condition, machining parameters, and feature geometry. Specifying a finer finish than necessary significantly increases cost.
Ra Value (um)	Ra Value (uin)	Typical Process	Application	Relative Cost
6.3	250	Rough milling / turning	Non-critical surfaces, hidden faces	1x (baseline)
3.2	125	Standard milling / turning	General machined surfaces (as-machined default)	1x
1.6	63	Finish milling / turning	Mating surfaces, bearing surfaces, visible surfaces	1.5x
0.8	32	Fine finish pass / grinding	Precision fits, seal surfaces, hydraulic bores	2-3x
0.4	16	Grinding / lapping / polishing	Precision bearing journals, optical mounting surfaces	4-6x
0.2	8	Lapping / superfinishing	Gauge blocks, precision optics mounts	8-15x
0.1	4	Superfinishing / polishing	Mirror finish, semiconductor equipment	15-30x

Surface Finish Guidance
The industry-standard as-machined finish is Ra 3.2 um (125 uin). Unless otherwise specified, this is what most CNC shops will deliver. Only callout specific surface finishes on surfaces where they are functionally required (sealing surfaces, bearing surfaces, mating interfaces). Leaving non-critical surfaces at as-machined finish significantly reduces cost.

4.9 Slots and Grooves
Parameter	Recommended	Achievable	Notes
Minimum slot width	1.5 mm	0.5 mm	Narrow slots require small fragile tools
Max depth-to-width ratio	4:1	8:1	Deep narrow slots limit chip evacuation
Slot end radius	= Tool radius	Specified	Slotting with end mill leaves rounded ends; square ends need EDM
Minimum web between slots	= Slot width	0.5 x slot width	Thin webs deflect and chatter
Keyway width	Standard keyway sizes	Custom	Standard widths match standard broaches/end mills
Groove width (external)	1.5 mm min	0.5 mm	On turned parts; narrow grooves require form tools

5. Tolerancing Guidelines
Tolerances have an outsized impact on manufacturing cost. The following guidelines help designers specify tolerances that achieve the required function without unnecessary precision.
5.1 General Tolerance Classes
Tolerance Class	Linear Tolerance	Angular Tolerance	Typical Application	Relative Cost
Coarse	+/- 0.5 mm	+/- 1.0 deg	Non-functional, clearance features	0.5x
Medium (Standard)	+/- 0.13 mm (+/- 0.005")	+/- 0.5 deg	General machined features (default)	1x
Precise	+/- 0.05 mm (+/- 0.002")	+/- 0.25 deg	Mating surfaces, bearing fits	2x
High Precision	+/- 0.025 mm (+/- 0.001")	+/- 0.10 deg	Precision assemblies, optical mounts	3-5x
Ultra Precision	+/- 0.013 mm (+/- 0.0005")	+/- 0.05 deg	Gauge-quality, metrology equipment	5-10x
Grinding / Lapping	+/- 0.005 mm (+/- 0.0002")	N/A	Seal surfaces, gauge blocks	10-25x

5.2 Geometric Dimensioning & Tolerancing (GD&T)
GD&T provides a more precise way to communicate design intent than simple linear tolerances. The following table summarizes achievable values for common GD&T callouts on CNC machined parts.
GD&T Symbol	Characteristic	CNC Typical	CNC Best	Notes
◎	Flatness	0.05 mm / 100 mm	0.013 mm / 100 mm	Affected by part thickness and clamping stress
○	Circularity (Roundness)	0.013 mm	0.005 mm	Turned features; depends on spindle runout
//	Parallelism	0.025 mm / 100 mm	0.010 mm / 100 mm	Between two machined faces
⊥	Perpendicularity	0.025 mm / 100 mm	0.010 mm / 100 mm	Between features in same setup is tightest
⬡	Cylindricity	0.025 mm	0.008 mm	Requires precision turning or grinding
⌖	Position (Hole)	0.05 mm	0.013 mm	True position at MMC; depends on fixturing
⇑	Concentricity	0.025 mm	0.008 mm	Co-axial features; best in single setup
∥	Symmetry	0.05 mm	0.013 mm	Symmetric features about datum plane
∿	Profile of a Surface	0.05 mm	0.013 mm	3D surface tolerance; 5-axis capability helps
↗	Total Runout	0.025 mm	0.008 mm	Composite of circularity + concentricity

Tolerance Strategy
Apply the 80/20 rule: 80% of features should use the general (medium) tolerance, 15% may need precise tolerances, and only 5% or fewer should require high precision. Mark tight tolerances clearly on drawings and include a note explaining the functional reason. This communicates intent to the machinist and helps the shop optimize their approach.

6. 3-Axis Milling Guidelines
3-axis milling is the most common and cost-effective CNC milling process. The tool moves in X, Y, and Z while the workpiece remains fixed. All features must be accessible from a single direction per setup.
6.1 Design Constraints
•	Line-of-sight access: Every feature must be visible and accessible from directly above (along the tool axis). No overhanging or undercut features are possible without additional setups.
•	Maximum of 6 accessible faces: A prismatic part can be machined on all six faces, but each face requires a separate setup (flip). Minimize the number of faces requiring machining.
•	2.5D geometry preferred: Features with constant cross-section in Z (pockets, holes, slots) are fastest to machine. True 3D sculptured surfaces require ball-end milling with fine stepovers, significantly increasing cycle time.
•	Vertical walls are standard: Walls perpendicular to the machine table are natural for 3-axis milling. Angled walls require ball-end mills or tapered end mills.
•	Floor fillets depend on tool: The transition between a vertical wall and a horizontal floor always has a fillet equal to the ball nose radius of the tool used.
6.2 Recommended Envelope and Capacity
Parameter	Typical Range	Notes
Maximum part size	1000 x 500 x 500 mm	Standard VMC; larger parts require horizontal or gantry mills
Minimum feature size	0.5 mm	Limited by smallest available end mill
Typical positional accuracy	+/- 0.025 mm	Modern VMC with probing
Typical surface finish (milling)	Ra 1.6 - 3.2 um	As-machined with new tooling
Maximum tool length (practical)	150 mm (6")	Longer tools deflect; affects accuracy and finish
Typical number of setups	2-6	Top + bottom minimum; more for features on multiple faces

7. 4-Axis Milling Guidelines
4-axis milling adds a rotary axis (typically the A-axis, rotating around X) to the three linear axes. This enables machining features on multiple faces of a part in a single setup, particularly for cylindrical or prismatic parts mounted on a rotary table or indexer.
7.1 When to Design for 4-Axis
•	Parts with features on 3 or more faces that would otherwise require multiple setups.
•	Cylindrical parts with features at multiple angular positions (ports, flats, holes).
•	Parts requiring continuous rotary machining (helical features, cam profiles, turbine blades).
•	Parts where inter-feature angular position tolerance is critical (easier to hold in one setup).
7.2 Design Rules for 4-Axis
Parameter	Guideline	Notes
Rotary axis clearance	Ensure tool clears rotary table at all angles	Check for interference between tool, part, and fixture
Angular position tolerance	+/- 0.05 deg typical	Indexing accuracy of rotary table
Feature orientation	Align features to cardinal angles (0, 90, 180, 270 deg)	Indexed positions are most accurate; continuous is less precise
Part balance	Balanced mass distribution preferred	Unbalanced parts cause vibration at high rotary speeds
Wrap-around features	Continuous 4-axis capable	Helical grooves, cam profiles possible
Fixturing	Central bore or shaft for mandrel mounting	Design a datum bore or shaft for rotary mounting

8. 5-Axis Milling Guidelines
5-axis milling adds two rotary axes to the three linear axes, enabling the tool to approach the workpiece from virtually any direction. This dramatically expands geometric freedom and often allows complex parts to be machined in a single setup.
8.1 Advantages of 5-Axis Machining
•	Single-setup machining of complex parts with features on multiple faces and angles.
•	Shorter tools due to optimal tool orientation, resulting in better rigidity, accuracy, and surface finish.
•	Ability to machine undercuts, compound angles, and sculptured surfaces impossible with 3-axis.
•	Improved surface finish on 3D contours through constant tool-surface contact angle.
•	Reduced number of fixtures and setups, improving positional accuracy between features.
8.2 Design Rules for 5-Axis
Parameter	Guideline	Notes
Tool approach angle	Min 15 deg from surface tangent	Shallow angles cause poor cutting and surface finish
Concave surface min radius	R > tool radius + 10%	Tool must fit within concavity with clearance
Impeller blade thickness	> 0.8 mm for aluminum	Thin blades deflect under tool load
Compound angle holes	Fully supported	5-axis tilts tool to drill perpendicular to angled surfaces
Turbine blade twist	Continuous 5-axis required	Ruled surfaces possible with 3+2; sculpted requires full 5-axis
Multi-face datum alignment	+/- 0.013 mm achievable	All features referenced to single datum in one setup
Collision avoidance	Min 5 mm tool-fixture clearance	CAM simulation essential; design fixturing with tool paths in mind
3+2 vs. simultaneous 5-axis	3+2 for indexed features	3+2 (positional) is more rigid and accurate than continuous 5-axis

5-Axis Cost Consideration
5-axis machining has a significantly higher hourly rate than 3-axis (typically 1.5x to 2.5x). However, it often reduces total cost by eliminating multiple setups, fixtures, and the tolerance stack-up between setups. Consider 5-axis when a part would require 4+ setups on a 3-axis machine, or when inter-feature positional accuracy is critical.

9. CNC Turning Guidelines
CNC turning produces rotationally symmetric parts using a rotating workpiece and a stationary or live cutting tool. Parts are held in a chuck or collet and features are generated along and around the axis of rotation.
9.1 General Turning Design Rules
Parameter	Recommended	Achievable	Notes
Min turned diameter	3.0 mm	0.5 mm (Swiss lathe)	Small diameters require Swiss-type machines or collet chucks
Max length-to-diameter ratio (unsupported)	4:1	8:1	Beyond 4:1 requires tailstock support or steady rest
Max L/D with tailstock	10:1	20:1	Tailstock center supports the free end
Diameter tolerance	+/- 0.025 mm	+/- 0.005 mm	Tight tolerances require precision boring or grinding
Length tolerance	+/- 0.05 mm	+/- 0.013 mm	Facing operations; limited by tool nose radius compensation
Concentricity (between diameters)	0.025 mm TIR	0.005 mm TIR	Best when machined in single chucking
Surface finish (OD turning)	Ra 1.6 um	Ra 0.4 um	Fine finish requires sharp inserts, low feed, high speed
Surface finish (boring)	Ra 1.6 um	Ra 0.4 um	Boring bar deflection limits achievable finish at depth
Minimum bore diameter	6 mm	3 mm	Limited by boring bar rigidity at depth
Max bore depth-to-diameter	4:1	8:1	Deep bores require dampened boring bars

9.2 Turning Feature Design
•	Chamfer all external sharp edges: 0.5 mm x 45 deg minimum. Chamfers facilitate assembly and eliminate hazardous sharp edges.
•	Include relief grooves before shoulders: A relief groove (undercut) at shoulders allows turning tools to reach full depth and ensures clean right-angle transitions.
•	Use standard insert nose radii: Common values are R 0.4, R 0.8, R 1.2, and R 1.6 mm. The tool nose radius appears as a fillet at corners and shoulders.
•	Center drill both ends of shafts: Center holes allow support between centers for grinding and inspection. Specify 60-degree center drill size A or B.
•	Knurling: Standard diamond and straight knurl patterns are available. Specify knurl pitch (e.g., 0.8 mm) and pattern. Knurled diameter grows by approximately 0.5x the pitch on radius.
•	Design for collet chucking: Parts requiring high concentricity should include a precision reference diameter for collet gripping.

9.3 Swiss-Type Turning
Swiss-type (sliding headstock) lathes are specialized for small-diameter, long, slender parts. The workpiece is supported by a guide bushing directly adjacent to the cutting zone, enabling extremely tight tolerances on long thin parts.
Parameter	Typical Capability	Notes
Part diameter range	1 - 32 mm	Most common 12 - 20 mm capacity
Length-to-diameter ratio	Up to 30:1	Guide bushing supports near the cut zone
Diameter tolerance	+/- 0.005 mm	Precision collet and guide bushing
Surface finish	Ra 0.4 um	Excellent due to guide bushing rigidity
Live tooling	Cross drilling, milling, polygon turning	Eliminates secondary operations
Ideal for	Fasteners, pins, shafts, medical, connectors	High-volume, small-diameter precision parts

10. Workholding Considerations
Proper workholding is essential for achieving dimensional accuracy and surface quality. Part design should always account for how the part will be fixtured during each machining operation.
10.1 Design-for-Fixturing Rules
•	Flat datum surfaces: Include at least one large flat surface for the first setup. This surface contacts the vise jaw or fixture plate and serves as the primary datum.
•	Parallel opposing faces: Two parallel faces enable vise clamping. Ensure adequate area and parallelism for secure gripping.
•	Minimum clamping area: Provide at least 10 mm of clamping surface in the vise direction. Parts too thin or too small require custom fixtures.
•	Avoid interrupted clamping surfaces: Holes, pockets, or slots on clamping faces reduce grip force and cause uneven pressure.
•	Soft jaw features: For round or irregular parts, include a datum diameter or flat that soft jaws can be machined to match.
•	Sacrificial tabs/bridges: For thin or fragile parts, design sacrificial material that holds the part during machining and is removed afterward.
•	Vacuum fixturing features: For thin plates, ensure one face is flat and smooth for vacuum chuck sealing. Seal path must be uninterrupted.

Workholding Tip
If you are unsure how a part will be held, add a note on the drawing asking the machine shop for a fixturing plan review. Many DFM issues can be resolved by adding small non-functional features (locating holes, alignment flats, or clamping tabs) that dramatically simplify workholding.

11. Secondary Operations
Secondary operations are processes performed after primary CNC machining to achieve properties or features not possible with machining alone. Proper design consideration for secondary operations prevents costly rework and dimensional issues.
11.1 Heat Treatment
Process	Typical Materials	Effect	DFM Considerations
Through Hardening	4140, 4340, 1045	Increases hardness and strength throughout	Machine before HT; leave 0.25-0.5 mm stock for finish grinding after HT due to distortion
Case Hardening (Carburize)	8620, 1018, 9310	Hard surface, tough core	Design masking areas for surfaces that must remain soft; min 2 mm wall for carburizing
Nitriding	4140, 4340, Nitralloy	Hard surface, minimal distortion	Excellent dimensional stability; minimal stock allowance needed
Induction Hardening	1045, 4140, 4340	Localized surface hardening	Design features to accommodate induction coil geometry; uniform cross-section preferred
Stress Relief	All steels, aluminum	Removes residual machining stress	Critical for tight-tolerance parts; perform between roughing and finishing
Aging / Precipitation Hardening	17-4 PH, 7075-T6, A286	Increases strength via precipitate formation	Machine in solution-treated condition; age after for optimal properties
Annealing	All metals	Softens material, relieves stress	Used before machining hard stock or between heavy machining operations
Cryogenic Treatment	Tool steels, bearing steels	Converts retained austenite; improves wear	Dimensional changes minimal; improves long-term stability

Heat Treatment Warning
Heat treatment causes dimensional changes. Case hardening and through hardening typically cause 0.05-0.25 mm of growth or distortion. For precision features, leave grinding stock (0.25-0.5 mm per side) and finish to final dimensions after heat treatment. Always specify the desired final hardness and depth on the drawing.

11.2 Surface Treatments and Coatings
Process	Typical Materials	Thickness Added	DFM Considerations
Anodize Type II (Standard)	Aluminum alloys	12-25 um total (50% penetrates, 50% builds up)	Grows ~0.013 mm per side; mask threads and tight-tolerance bores
Anodize Type III (Hard)	Aluminum alloys	25-75 um total	Grows ~0.025-0.038 mm per side; account in tolerances; very hard (60-70 HRC equivalent)
Chromate Conversion (Alodine)	Aluminum alloys	< 1 um	No dimensional change; excellent for electrical conductivity + corrosion protection
Electroless Nickel	Steel, aluminum, copper	5-75 um	Very uniform coating; builds up 0.005-0.075 mm per side; excellent corrosion resistance
Hard Chrome Plating	Steel, stainless	25-250 um	Builds up 0.025-0.25 mm per side; excellent wear resistance; must account in dimensions
Zinc Plating	Steel	5-25 um	Builds up 0.005-0.025 mm; hydrogen embrittlement concern on high-strength steels
Black Oxide	Steel, stainless	< 2 um	Negligible dimensional change; provides mild corrosion resistance and appearance
Passivation	Stainless steel	None (removes iron)	No dimensional change; improves natural corrosion resistance of stainless steel
Powder Coat	Steel, aluminum	50-150 um	Significant build-up; mask all precision surfaces and threads
Nickel Plating (electrolytic)	Steel, copper	10-50 um	Moderate build-up; less uniform than electroless; lower cost
Tin Plating	Copper, steel	5-25 um	Solderability; used for electrical contacts and connectors
PTFE Impregnated Anodize	Aluminum	12-50 um	Low friction coating; ideal for sliding surfaces; accounts same as Type II/III

11.3 Grinding
Grinding is used to achieve tolerances and surface finishes beyond standard CNC machining capability, typically after heat treatment.
Grinding Type	Tolerance	Surface Finish	DFM Considerations
Surface (flat) grinding	+/- 0.005 mm	Ra 0.2 - 0.8 um	Leave 0.25 mm grinding stock; ensure flatness datum; min 3 mm part thickness
Cylindrical OD grinding	+/- 0.005 mm	Ra 0.2 - 0.4 um	Include center holes for between-centers grinding; leave 0.2 mm stock on diameter
Cylindrical ID grinding	+/- 0.008 mm	Ra 0.4 - 0.8 um	Min bore diameter 6 mm; max depth 4x diameter; leave 0.15-0.25 mm stock
Centerless grinding	+/- 0.005 mm	Ra 0.2 - 0.4 um	Excellent for high-volume cylindrical parts; needs uninterrupted OD
Jig grinding	+/- 0.003 mm	Ra 0.2 - 0.4 um	Precision hole location and profile; very high cost

11.4 EDM (Electrical Discharge Machining)
EDM is used for features that are impossible or impractical with conventional CNC machining, particularly in hardened steels and complex internal geometries.
EDM Type	Tolerance	Surface Finish	Best Applications
Wire EDM	+/- 0.005 mm	Ra 0.4 - 1.6 um	Through profiles, gears, splines, sharp internal corners, hardened steel
Sinker (Ram) EDM	+/- 0.013 mm	Ra 0.8 - 3.2 um	Blind cavities, ribs, textures, complex 3D shapes in hard materials
Hole drilling EDM	+/- 0.025 mm	Ra 3.2 - 6.3 um	Small deep holes, cooling holes in turbine blades, start holes for wire EDM

EDM Design Tip
Wire EDM can produce perfectly sharp internal corners, which is impossible with rotary cutters. If sharp internal corners are functionally required (e.g., for splines, keyways, or gear teeth), specify wire EDM for those features. However, note that wire EDM requires through-features (the wire must enter and exit the workpiece). For blind sharp-cornered pockets, sinker EDM is required.

11.5 Deburring
All machined edges produce burrs to some extent. Design choices can significantly affect deburring cost and ease.
•	Intersecting holes: The intersection of two holes creates a burr on the inside of the smaller hole that is extremely difficult to remove. Avoid or minimize intersecting holes; if required, specify acceptable burr height.
•	Cross-drilled holes: Port intersections on hydraulic manifolds are a common burr challenge. Design for thermal deburring (TEM) or abrasive flow machining (AFM) access if critical.
•	Chamfer all accessible edges: A 0.25-0.5 mm chamfer on the drawing preemptively removes the edge that would otherwise carry a burr.
•	Tumble-friendly geometry: If parts will be tumble-deburred, avoid features that trap media (deep blind holes, narrow slots, small pockets).
•	Specify burr height tolerance: For critical applications (medical, aerospace), specify maximum allowable burr height (e.g., 0.05 mm max).

12. Common DFM Violations Checklist
Use this checklist to review designs before release to manufacturing. Each item represents a frequent design error that increases cost, delays delivery, or reduces quality.
#	Violation	Impact	Resolution
1	Sharp internal corners (zero radius)	Impossible to machine with rotary cutters	Add fillet radius >= tool radius + 10% clearance
2	Deep pockets with small radii	Requires long, thin tools that deflect and chatter	Increase radius or reduce depth; depth:width <= 4:1
3	Thin walls adjacent to deep pockets	Vibration, deflection, potential wall failure	Increase wall thickness or reduce pocket depth
4	Unnecessarily tight tolerances on non-functional features	Dramatically increases cycle time and cost	Apply tight tolerances only where functionally required
5	Non-standard hole sizes	Requires reaming or interpolation instead of standard drills	Use standard drill sizes (fractional, metric, or letter)
6	Non-standard thread sizes	Requires thread milling instead of stock taps	Use standard metric coarse or UNC thread sizes
7	Flat bottom blind holes without specifying	Requires separate end mill operation after drilling	Accept drill-point bottom or explicitly callout flat bottom
8	Text or logos on machined surfaces	Requires engraving or EDM; adds significant time	Minimize text; use simple sans-serif fonts; specify depth
9	Undercuts that can be redesigned away	Requires special tooling and often manual operations	Redesign to eliminate undercuts wherever possible
10	No datum surfaces or fixturing features	Part cannot be securely held or accurately located	Add parallel faces, locating holes, or reference datums
11	Specifying surface finish on all surfaces	Entire part must be finish-machined	Only specify finish where functionally required
12	Overly complex geometry that could be split into two parts	Extreme tool access issues and many setups	Consider multi-piece assembly for complex geometries
13	Holes drilling into angled or curved surfaces	Drill walks on angled entry; poor position accuracy	Add a local flat (spot face) or specify centering operation
14	Thread depth exceeding 2x diameter in blind holes	High risk of tap breakage and difficult chip evacuation	Limit thread depth to 1.5-2.0x diameter
15	Inconsistent fillet radii throughout the part	Excessive tool changes increase cycle time	Standardize on 2-3 fillet radii matching standard tool sizes

13. Cost Optimization Strategies
This section provides actionable strategies for reducing CNC machining cost without compromising functional requirements.
13.1 Design-Level Strategies
1.	Minimize number of setups: Design features accessible from as few orientations as possible. Each setup adds 15-30 minutes of non-cutting time.
2.	Use standard stock sizes: Design parts to be cut from standard bar, plate, or tube sizes. Minimize face-off material and reduce raw material waste.
3.	Avoid deep pockets: Reducing pocket depth from 50 mm to 25 mm can cut cycle time by 60% or more due to fewer passes and less material removal.
4.	Design near-net-shape: Start with stock that closely matches the final part envelope. Consider extrusions, castings, or forgings as raw stock for high-volume parts.
5.	Reduce the number of unique tools needed: Each tool change adds 5-15 seconds per part. Standardize features to use the same tools.
6.	Relax tolerances: Moving from +/- 0.025 mm to +/- 0.13 mm on non-critical features can reduce machining time by 30-50%.
7.	Batch-friendly design: Design parts to be machined in multiples per setup (gang machining) or from a single workpiece (multi-part nesting).
8.	Avoid cosmetic machining: Leave non-visible surfaces as-machined. Decorative features (chamfered edges, polished surfaces) add significant time.

13.2 Material-Level Strategies
•	Choose free-machining alloys: Switching from 304 stainless steel to 303 stainless steel can reduce cycle time by 30-40% with negligible mechanical property difference.
•	Pre-hardened materials: Using pre-hardened 4140 (28-32 HRC) eliminates post-machining heat treatment for many applications.
•	Material substitution analysis: Aluminum can often replace steel for non-structural components, cutting machining time by 60-70% and reducing weight.
•	Consider material form: Tube stock for hollow cylindrical parts, angle stock for bracket-shaped parts, and extruded profiles for channel shapes reduce material removal significantly.

14. Drawing and Documentation Best Practices
Clear, complete engineering drawings are essential for successful manufacturing. Ambiguous or incomplete drawings lead to delays, errors, and increased cost.
14.1 Required Drawing Information
•	Material specification: Full material callout including alloy, temper/condition, and specification (e.g., Aluminum 6061-T6 per AMS QQ-A-250/11).
•	General tolerance block: Define default tolerances for all features not explicitly dimensioned.
•	Surface finish: Default surface finish (typically Ra 3.2 um as-machined) plus specific callouts on critical surfaces.
•	Heat treatment requirements: Specify the desired condition and hardness range (e.g., Heat treat to 28-32 HRC per AMS 2759).
•	Surface treatment / coating: Full callout including spec, type, class, and color where applicable (e.g., Anodize Type II, Class 2, Black per MIL-A-8625).
•	Thread callout: Thread size, class, and depth for all threaded features.
•	Deburr and break edges: Standard note: Break all sharp edges 0.25 mm max unless otherwise specified.
•	Part marking: Specify method (engrave, etch, stamp), location, size, and content for part identification.
•	Inspection requirements: Identify critical dimensions requiring first article inspection (FAI) or certificate of conformance (CoC).

15. Reference Tables
15.1 Standard Metric Drill Sizes
The following metric drill sizes are universally stocked by CNC machine shops. Using these sizes avoids reaming and reduces cost.
Diameter (mm)	Diameter (mm)	Diameter (mm)	Diameter (mm)
1.0	3.5	7.0	13.0
1.5	4.0	8.0	14.0
2.0	4.5	9.0	16.0
2.5	5.0	10.0	18.0
3.0	6.0	12.0	20.0

15.2 Tap Drill Sizes (Metric Coarse Threads, ~75% Thread)
Thread	Tap Drill (mm)	Thread	Tap Drill (mm)
M3 x 0.5	2.5	M10 x 1.5	8.5
M4 x 0.7	3.3	M12 x 1.75	10.2
M5 x 0.8	4.2	M14 x 2.0	12.0
M6 x 1.0	5.0	M16 x 2.0	14.0
M8 x 1.25	6.8	M20 x 2.5	17.5

15.3 Standard End Mill Diameters
Use these standard diameters when specifying internal corner radii and pocket widths to ensure standard tooling can be used.
Metric (mm)	Imperial (inches)	Metric (mm)	Imperial (inches)
1.0	1/16" (1.59 mm)	10.0	3/8" (9.53 mm)
2.0	3/32" (2.38 mm)	12.0	1/2" (12.7 mm)
3.0	1/8" (3.18 mm)	16.0	5/8" (15.88 mm)
4.0	3/16" (4.76 mm)	20.0	3/4" (19.05 mm)
5.0	1/4" (6.35 mm)	25.0	1" (25.4 mm)
6.0	5/16" (7.94 mm)	32.0	1-1/4" (31.75 mm)
8.0	N/A	40.0	1-1/2" (38.1 mm)

15.4 Unit Conversion Quick Reference
Conversion	Value	Conversion	Value
1 inch	25.4 mm	1 mm	0.03937 inches
1 thou (0.001")	0.0254 mm	0.01 mm	0.000394 inches
Ra 1 um	~40 uin	Ra 3.2 um	~125 uin
1 N·m	8.85 in·lbf	1 ft·lbf	1.356 N·m
1 MPa	145 psi	1 ksi	6.895 MPa
1 kg	2.205 lbs	1 lb	0.4536 kg

Appendix A: DFM Review Workflow
The following workflow outlines the recommended DFM review process for new part designs.
9.	Initial Design Concept: Complete 3D model with all functional features defined. Material selected. Operating loads and environment documented.
10.	Internal DFM Self-Check: Designer reviews part against guidelines in Sections 4 through 9 of this document. All feature dimensions checked against recommended values. Tolerances reviewed using Section 5 guidelines.
11.	Manufacturing Consultation: 3D model and preliminary drawing sent to manufacturing engineering or preferred CNC vendor for DFM review. Specific questions about challenging features highlighted.
12.	DFM Feedback Integration: Design modifications made based on manufacturing feedback. Trade-offs documented (e.g., feature cost vs. functional requirement).
13.	Final Drawing Release: Complete drawing with all information per Section 14. GD&T applied per Section 5. Material, finish, and treatment specifications complete.
14.	First Article Inspection (FAI): First production part inspected against drawing. Any out-of-tolerance features reviewed for drawing error vs. manufacturing issue. Drawing or process updated as needed.

Appendix B: Glossary of CNC Machining Terms
Term	Definition
Chatter	Vibration between the tool and workpiece that produces a rough surface finish and tool wear; often caused by thin walls, long tool extensions, or aggressive cutting parameters.
Chip Load	The thickness of material each cutting edge removes per revolution. Optimal chip load balances surface finish, tool life, and material removal rate.
Climb Milling	Milling where the cutter rotation is in the same direction as feed travel. Preferred for CNC machines; produces better finish and longer tool life.
Conventional Milling	Milling where the cutter rotation opposes feed direction. Causes more deflection and heat but is sometimes preferred for hard materials.
Depth of Cut (DOC)	The axial depth of material engagement per pass in milling, or radial depth in turning.
Dwelling	Holding the tool at a position momentarily. Used to improve surface finish at the bottom of bored holes.
End Mill	A rotary cutting tool for milling operations. Available in flat-end, ball-nose, corner-radius, and specialty profiles.
Feed Rate	The speed at which the cutting tool advances through the workpiece, typically in mm/min.
Fixture	A workholding device that locates, supports, and clamps the workpiece during machining.
G-Code	The programming language used to control CNC machines. Defines tool paths, speeds, feeds, and operations.
Guide Bushing	A precision bushing on Swiss-type lathes that supports the workpiece adjacent to the cutting zone.
Helix Angle	The angle of the cutting flutes on an end mill. Higher helix angles (40-45 deg) produce smoother cuts in aluminum.
Interpolation	Synchronized multi-axis movement to create circular or contour tool paths.
Live Tooling	Rotating cutting tools on a lathe that enable milling, drilling, and tapping without removing the part from the chuck.
Peck Drilling	A drilling cycle where the drill retracts periodically to clear chips. Essential for deep holes.
Runout	The total variation in the position of a rotating surface measured at a fixed point. Affects concentricity and surface finish.
SFM / SMM	Surface Feet per Minute / Surface Meters per Minute. The speed at which the cutting edge moves across the workpiece surface.
Spot Drill / Center Drill	A short rigid drill used to create a starting point (pilot hole) for a subsequent drill to prevent walking.
Step-Over	The radial distance between adjacent tool paths in area milling. Smaller step-over gives better surface finish but longer cycle time.
Tailstock	A support at the opposite end of a lathe from the chuck. Provides center support for long workpieces.
TIR (Total Indicated Runout)	The full range of indicator reading when measuring a rotating feature. Used to express concentricity and coaxiality.
Tool Deflection	The bending of a cutting tool under cutting forces. Increases with tool length and decreases with tool diameter.
Work Envelope	The maximum XYZ travel of a CNC machine. Parts must fit within this volume.

300 Riverpark Drive, North Reading, MA 01864
Title: DESIGN GUIDELINE, HIGH PRESSURE DIE CAST AND GRAVITY CAST PERMANENT MOLD
DOCUMENT NUMBER: 930-00166
REVISION: 01
PROCESS OWNER: ADVANCED MANUFACTURING ENGINEERING Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 2 of 20
Table of Contents
DESIGN GUIDELINE, HIGH PRESSURE DIE CAST AND GRAVITY CAST PERMANENT MOLD ........................... 3
Fabrication process overview ................................................................................................................... 3
Primary Differences Between High Pressure Die Casting and Permanent Mold ...................................... 5
Process Comparison: High Pressure Die Cast vs Permanent Mold ....................................................... 7
Applicability of processes based on design stability or development phase ........................................... 7
Design for casting guidelines .................................................................................................................... 8
Gates and Vents/Risers ............................................................................................................................. 8
Parting Lines ............................................................................................................................................ 10
Consistent/Uniform Wall Thickness, Promoting Good Part Fill. ............................................................. 11
Corner Radii and Fillets ........................................................................................................................... 12
Draft ........................................................................................................................................................ 12
Undercuts and 0 degree draft conditions. .............................................................................................. 13
Cast part Geometry consideration for CNC ............................................................................................ 14
Other Cast Feature Design Considerations ......................................................................................... 15
Materials and Finishes ............................................................................................................................ 16
Materials ............................................................................................................................................. 16
Finishes................................................................................................................................................ 17
Process capabilities ................................................................................................................................. 18
Secondary operations ............................................................................................................................. 19
Cost drivers ......................................................................................................................................... 19
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 3 of 20
DESIGN GUIDELINE, HIGH PRESSURE DIE CAST AND GRAVITY CAST PERMANENT MOLD
Fabrication process overview
Gravity Fed Permanent Mold (Perm Mold) and High Pressure Die Casting (HPDC or Die Casting) are two metal fabrication techniques commonly used at Amazon Robotics in the production of non-ferrous metal components. At Amazon Robotics, the material typically used is typically aluminum, but can also include magnesium, zinc and other metals. These processes are not suitable for iron, steel, stainless steel. This guideline will consider aluminum as the material for casting. Variances in processing and design consideration for magnesium and zinc should be investigated separately if a particular project has a need.
The as-cast part is not suitable for applications at AR without additional machining. Higher precision surfaces and features are created using post-Cast CNC machining on the part (CNC machining to be discussed in a separate design guideline). Parts can be left “raw” or finished with a variety of treatments.
The process flow can be represented as:
Brief description of each process step
• Material Prep: Aluminum is melted and degassed in preparation for casting. Degassing involves introducing inert gas into the molten aluminum to reduce reaction air and moisture which would allow hydrogen to be absorbed into the aluminum which would turn into trapped bubbles as the melt solidifies.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 4 of 20
• Casting: Molten aluminum is introduced into the mold by either gravity (Perm Mold) or via raminduced
pressure (cold chamber high pressure die casting)
• Cast finishing. Gates and vents are removed with trim dies and manual or automated grinding
processes.
• Finishing (pre or post-CNC): Depending on the requirements for finish (powder coat, anodize, ecoat,
chromate, etc), the castings can be finished either before or after CNC
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 5 of 20
• CNC Machining: Higher precision surfaces and features are created using post-Cast CNC machining on the part. CNC machining design guidelines will be part of a separate document.
Primary Differences Between High Pressure Die Casting and Permanent Mold
In both cases, two-part steel molds1 are fabricated. The mold halves are held together, then filled with molten metal to create a net shape part, once the part has cooled sufficiently, the mold is opened and the part removed.
• In the case of Permanent mold (also known as gravity casting), the two halves of the mold are painted/coated with ceramic paint, clamped together and molten metal is poured into the mold.
Gravity pulls the molten metal to the bottom of the mold and the part is filled from the bottom up (hence the term, gravity casting). The ceramic paint is used for thermal management within the mold and causes directional solidification of the molten aluminum as well as improving the flow/fill of the molten aluminum.
• In the case of High Pressure Die Casting, molten metal is loaded into the die casting press and is hydraulically pushed into the mold with an injection piston at high speed and high pressure. The two halves of the mold are hydraulically clamped together. Hydraulic clamping is required to manage the high injection pressure (typically around 8Kpsi). Each square inch of the cast part (including gates, runners, vents) requires 4 tons of clamping pressure. Die casting presses are referenced as to their clamping force in terms of tonnage. Our supply base currently has machines with clamping force up to 4400 tons
1 While molds are traditionally considered 2-part open and shut with a traditional core (drag) and cavity (cope) side comprising the two halves of the mold, molds are much more complex than this with ejection systems, options for side action created by slides and other mold components. Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 6 of 20
On past projects AR has had a bias towards die casting to leverage piece part advantage, unless the
production demands are low quantity. Permanent mold has traditionally been used on very large,
structural parts with thick cross-sections that cannot be achieved with HPDC such as the H-DU front
chassis, turntable top/bottom or the S-DU chassis castings.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 7 of 20
Process Comparison: High Pressure Die Cast vs Permanent Mold
HPDC
Perm
Mold Notes
Profile
Tolerance
✓
E-W claims as tight as 0.5mm on same side of tool for HPDC, but is part size dependent
For reference: HPDC profi le on H-DU panhard and tiebards is 0.75mm, on H-DU rear
chassis 1.5mm
Perm mold on H-DU front chassis and rotary table is 2.6mm, 3.6mm across parting l ine
Dimensional
Tolerance-as
cast
✓
Publ ished tables show HPDC at .002mm/mm of length tolerance, Perm Mold at .38mm +
.002mm/mm tolerance
Across parting l ine: HPDC additional 0.25mm. Perm Mold additional 0.76 to 1mm.
Part size, across parting l ine or to movable sl ide al l impact tolerance
Part Strength ✓
HPDC cast material is 30-50% stronger than gravity casting equivalents (before HT). With
heat treatment, gravity castings can approach but not quite meet a HPDC strength (maybe -
5-10%) when considering simi lar geometery between HPDC and Perm Mold.
However given abi l ity to cast much thicker cross sections in Perm Mold, the abi l ity to
create a stronger part favors Perm Mold.
Surface finish
and Draft
✓ 60-120 RMS for HPDC vs 250-420 RMS typical for Perm Mold.
Draft ✓ Required draft is higher for Perm Mold to reduce risk of sticking. 1 to 1.5 degrees for
HPDC, 1-3 degrees or more for Perm Mold
Minimum
nominal ascast
wall
thickness
3-10 mm
4mm and
thicker
Max part size ✓
Max HPDC part size is driven by max 4400 ton press size at our preferred suppl ier, which
equates to ~5500cm^2 maximum projected part surface area at the time of publ ishing on
the larger side of the part.
AR uses Perm Mold for parts larger than this
Tooling Cost ✓
Tooling
Leadtime
✓
Casting cycle
time
HPDC Cycle times are in the 60-100 second range (dependent upon part size)
Perm Mold times are in the 240-280 second range (dependent upon part size)
Piece Part
Cost
✓ HPDC has faster fi l l times and lower part production cycle times and is usual ly more
competitive than perm mold
Tool life ✓
We cap tool l ife for HPDC at 100K shots due to mold degradation (heat checking for
instance)
We manage perm mold tool l ife to 60K shots
Al l things simi lar (part size, tool ing location-US, Asia, etc) Perm Mold tool ing cost and
leadtime are less since the tool ing is simpler than HPDC
Historical tool ing costs: HPDC: $15k-300K+, Perm mold: $10K-60K+
Nominal Leadtimes: HPDC: samples = 12-26 weeks; production = 3-6 weeks after approval
Perm mold: samples = 12-16 weeks; production 3-6 weeks after approval
Applicability of processes based on design stability or development phase
Both High Pressure Die Casting and Permanent Mold are production manufacturing processes. Even
lower volume AR-DUs (drive units) in the 10K EAU range will justify the tooling investment to yield a high
performing, lower cost part than can be achieved with fabrication techniques suitable for prototyping or
lower volume where the tooling investment is not justified. Depending on the part requirements and
complexity, a cost tradeoff between perm mold and other low volume cast or CNC processes may show
perm mold as cost effect at as low as 1000 pieces annually.
Tooling for permanent mold or HPDC ranges from the $10,000’s upwards of $500,000+ depending on
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 8 of 20
the part size and complexity of trimming and CNC fixtures. Alternate fabrication processes for prototyping or low volume include:
• V-process casting. The closest approximation to the structural performance and finish of an HPDC or perm mold.
• Rubber plaster or plaster molds
• Sand casting
• CNC machining. For low volume or cases where you do not need to have a cast part to replicate as-cast performance, CNC is a suitable alternative for smaller parts with competitive pricing from Asia.
Design for casting guidelines
Key References: NADCA Product Specification Standards for Die Castings - 11th Edition Standards for Aluminum Sand and Permanent Mold Castings - 16th Edition 2021 While there are some tolerance and finish limitations with Permanent Mold compared to Die Casting (see table above), the majority of design best practices are common across both manufacturing processes. Many of the basic design principles of Perm Mold and HPDC are common with injection molding. A two-piece mold is created with a negative space void to be filled with aluminum (or other metal) or plastic in the case of injection mold. The mold is held shut during casting/molding, and then opened once adequate cooling has occurred. The part is then ejected out of the mold.
Gates and Vents/Risers
Gates (where the molten metal is introduced into the mold for filling) and vents or risers (where air within the mold is evacuated and excess molten metal is allowed to flow to ensure part fill) are elements of a cast part to consider during part design. Ultimately the supplier will drive the decision on gate and venting, but having basic knowledge of strategy may help through the design process and DFM. Die casting:
• Gate location will set the general direction of material flow into the part. Material flow direction is usually determined based upon orientation of least resistance to part fill. Impediment to good Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 9 of 20
fill of a part may be changes in part thickness, holes in part, features which sit orthogonal to planned direction of fill.
• Venting is used to promote part fill and “steers” material flow
See comparison below of two similar parts with different gate orientation. Rear chassis flow will be more direct along the axis of the hinge arms, while the Front chassis flow is better across the part due to the general orientation of ribbing and pockets in the part. In both designs, venting is added to ensure good fill in proximity to the gates (see red circles). Also notice the location of the parting line in red-dashed line and how gating and venting are along the parting line edge of the part.
The basic principles of gating and part orientation relative to gates are similar for both die cast and perm mold. Impediments to flow include ribbing orthogonal to flow direction, large holes which divert flow paths. Orthogonal ribbing flow disruption can be mitigated by feeder ribs added in the direction of flow if the design can accommodate. In the case of holes impeding flow, material bridges can be added and machined out alter.
Perm Mold: Due to the gravity fed nature of a permanent mold part with molten metal being poured in rather than rammed in under pressure, gate and riser schemes for permanent molds are typically larger in geometry with a smaller number of risers than comparable die cast vents.
• Gate system: Part orientation and gate location optimized to eliminate the risk of trapped air in a gravity fed system Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 10 of 20
• Vents/Risers: Allow air to escape the mold cavity and provide overflow to ensure part fill. Simplified views of a gravity fed systems shown below.
Parting Lines
The parting line is the perimeter on the casting which is the separation point of the two halves of the die casting mold. The parting line defines the draft plane in the part, so needs to be carefully considered during part design. In the example, it follows the red line shown.
While complex parting lines may be required to accommodate the product design, there are advantages to keeping parting lines as simple as possible, with options considered to trade off between part design and mold complexity.
• Simplified tooling (cost and leadtime)
• Since gates and vents are required for casting and are at the parting line, trim dies will be easier to design and fabricate on a part with a simple parting line than a complex one.
• Tool life, fit and finish. It is easier to maintain a planar parting line than a complex one.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 11 of 20
The following example shows decision making tradeoffs between part design, draft and parting line complexity.
Consistent/Uniform Wall Thickness, Promoting Good Part Fill.
Maintaining consistent wall thickness promotes good material flow and part fill. This is critical in die casting. Permanent molding using a gravity feed enables additional mold fill as material starts to cool Where thickness changes must occur, avoid abrupt thickness transitions. Abrupt changes create material turbulence and pressure changes which can result in porosity. Thick sections are also susceptible to porosity in die castings since air bubbles can form in thick sections as material cools/contracts. This is referred to as “shrink porosity”.
Hanging/isolated features. Hanging features are considered part features which are freestanding, yet adjacent to other features. When possible, these features should be bridged with material to those adjacent features to promote material flow. Other reasons for bridging would be to eliminate areas of thin mold steel. See the Minimum Feature Size section below
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 12 of 20
Corner Radii and Fillets
Both internal and external corners in a cast part should have radii added.
Minimum inside R of 0.5mm is a good general practice on die cast parts. If this cannot be achieved, any radius is better than leaving a sharp corner in the product design. External radii to match the inside R + wall thickness. This helps to maintain uniform wall thickness. Reasons for adding radii include:
• Sharp corners in the mold that create inside R in a part are impossible to maintain over the life of the mold.
• Sharp inside corners in both the part and the mold are stress concentrators.
• Sharp inside radii
Exceptions: Edges at the parting line (or other places where different parts of the mold meet) shall not have radii unless the function of the component requires a radius (ie-sharp edge that will be handled, etc.). In this case, a detailed DFM review is required to make sure mold design best practices are followed.
Draft
In general, vertical walls cannot be left vertical in the axis of the mold opening/closing. Molten metal and plastic shrink when they cool, which results in the part sticking against the core side of the tool. In addition, surface roughness creates additional points of friction between the cast part and the core and cavity of the mold. Without draft, a vertical wall on the cast component and the vertical wall of the mold will have significant friction to overcome when trying to remove the cast part from the mold (the process of part removal from a mold is called ejection). This friction can cause part warpage or breakage upon ejection and can result in a cast part being stuck on the core. Adding draft to the part reduces the amount cast part to mold interface. As the part starts to eject from the mold, the drafted surfaces on the mold and the cast part immediately separate.
Draft is critical to consider during part design since part geometry can be affected in ways that effect wall thickness, or interfaces to mating parts.
General draft guidelines:
• Die cast parts: Assume 1.5 degrees minimum draft. There may be cases where more or less draft may be required and can be determined during a supplier DFM review. Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 13 of 20
• Perm mold: Assume 3.0 degrees minimum draft. There may be cases where more or less draft may be required and can be determined during a supplier DFM review.
Note: For walls that need to be truly vertical, consider post-CNC machining on interior walls and/or adding slides/side action on exterior surfaces.
Undercuts and 0 degree draft conditions.
Undercuts in die casting are part features that cannot be manufactured with a simple two-part mold, because material is in the way while the mold opens or during ejection.
0 degree draft refers to the state outlined in the “draft” section above where a wall in the direction of mold open/close is not drafted to enable part ejection
Managing undercuts
• Side action/slides: These are additional pieces of tool steel used to create the undercut and are moved out of the way either automatically or manually. There is a tooling cost increase to add a slide (10% of tool cost is a good budgetary value)
• Post-casting CNC. These features can be machined in after casting. The additional cost of CNC can be quantified to compare to the additional mold cost for a slide.
• Other options: Ejection Lifter or Pass core. These are not common with our primary supply base for die casting. Consult your supplier for more feedback on feasibility.
An example of an AR part with both undercut and 0 draft conditions is 420-06155 ENCLOSURE, ARIMA, H-DU
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 14 of 20
Basic mold construction may be an aid to visualize how side action is implemented in a mold
Tool movement includes
1. The slide moves out of the way to eliminate the undercut situation. Depending upon the mechanism employed to create movement, it may occur concurrently with #2 below.
2. Core (with cast part) moves away from the cavity side of the mold.
3. The cast part is ejected from the core side of the mold.
Side action/slide considerations.
• Slides impact tooling cost and leadtime -avoid if possible
• Tolerance: When considering tolerance, use tolerances ‘across parting line“ or ”from fixed steel to movable steel“. There is additional tolerance to consider. Post-cast CNC may be required to achieve the needed accuracy.
• Consider side action and CNC processes together. While side action in a tool can eliminate post machining of casting, an analysis should always be completed to justify using a slide instead of using CNC operations to achieve the desired geometry.
Cast part Geometry consideration for CNC
As noted, post-cast CNC machining of cast parts is common to achieve tighter tolerances, smoother finishes or in areas where the needed features cannot be cast. Some things to factor into as-cast design: Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 15 of 20
Adding material for CNC machining. For cast surfaces that need to be machined for precision or finish reasons, additional “over-cast” material must be added to ensure that there is sufficient cast material to machine to the required dimension. This extra metal is commonly referred to as “machining stock”.
• For die casting: add 1mm of over-cast material. Do not add excess material since the deeper a part is machined from the skin, the greater risk of hitting porosity.
• For perm mold. add 1.5-2mm of over-cast material. Excess material is less risky with perm mold due to reduced risk of porosity, however, excess material will impact CNC time.
Air cuts. To mitigate risk of profile tolerance issues in critical areas due to tool wear which will increase surface size, an “air cut” can be specified that will include a CNC cutter path at maximum material condition.
Other Cast Feature Design Considerations
• Minimum wall thickness
o Die cast:
▪ Nominal 3mm (but thicker preferred)
▪ Minimum feature thickness: 2.0mm
o Perm Mold
▪ Nominal 4 mm (but thicker preferred)
▪ Minimum feature thickness: 3-4 mm with supplier feedback
• Minimum mold steel thickness (feature to feature gap)
o Die cast: 3mm (but thicker preferred)
o Perm Mold: 6mm if height of mold is 20 mm, but can go thinner if mold feature is shallower. Respect ~1:3 tool steel width:height ratio
• Resultant approximate fin pitch (factor in draft) when designing heat sinks
o Die cast: 2.5mm fin top + 3mm tool steel gap + 2 degrees draft (rib height*sin2 degrees)*2 ribs (note:it is possible to have more aggressive fin pitch with a tradeoff in tool life if tall, narrowly spaced fins are required, with concepts up to 80mm tall, 1.6mm wide at top, 1.5 degrees draft having been explored)
o Perm Mold: 3mm fin top + 4mm tool steel gap + 2 degrees draft (rib height*sin2 degrees)*2 ribs
• Minimum as-cast hole diameter.
o Die cast: For holes 5mm DIA or larger, cast the hole. For holes <5mm DIA, they should be created with post- cast CNC. For finished holes right at the 5mm DIA boundary, review with your supplier since profile tolerance needs to be considered.
o Perm Mold: Minimum as-cast hole diameter driven by maintaining adequate draw and draft angle as well a flow path of pour. As-cast hole diameter depends on final hole depth. Consult supplier for proper blind hole diameter and depth ratio.
• Unusual part geometry. Highlight parts for early DFM that have flat sections without ribbing, parts with large asymmetry, etc. These may have a larger propensity for warp. Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 16 of 20
• Ejector pin pads. For molds using ejection systems (all die cast molds), there may be areas where circular flat pads need to be added to the part to enable part ejection. These are often prevalent on parts which do not have large surface area orthogonal to direction of ejection
• Datum pads. Cast datums should be established on the same side of the die half, either cavity side or core side. These as-cast datums are used for as-cast inspection and for any initial CNC operations which are based off of them (including establishing as-machined datums). As the mold tool begins to wear, the variability across the parting line will grow. Therefore, keeping the cast datums on one side will prevent the datum reference frame from varying over time. Choose the die half with the most functional requirements or mating features. Avoid selecting cast datums features that are subject to variability like ejector pins, areas near parting lines, vents, and gates. Select cast datum features that will not become machined in order to maintain traceability of datums from cast to machined. As part datum strategy is developed, consider adding flat pads if possible on surfaces that are not orthogonal to datum structure. This works well on surfaces orthogonal in the direction of mold open/close. To maintain the ability to re-inspect a finished part, cast datums should always be kept on the part itself, not on tabs that will be machined off in later processes.
Materials and Finishes
Materials
The primary alloys of aluminum we use for casting include:
Die Casting:
• A380. General purpose alloy used in the majority of die castings at AR
• AlSi12(Fe). A newer (to AR) alloy with improved thermal conductivity properties. ~ 30% better thermal conductivity than A380 with a minor sacrifice in material properties
Permanent Mold: The primary alloy used on our permanent molded parts is 319.0 Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 17 of 20
Finishes
There are a variety of finishes which can be utilized for both decorative and functional applications
Finish Description Cosmetics Cost
Electrically
Conductive?
Corrosion
Protection?
Apply Pre-CNC
machine?
Color options? Notes
Raw Casting As-cast part
As-cast. Not
great
None
Yes-but risk of
oxidation
No N/A N/A
Chromate
Conversion
Corrosion
protection. Can be
electrically
conductive
depending on the
level of corrosion
Not used for
cosmetic
reasons
$
Can be applied
to be
conductive or
as an
insulator
Yes
Yes if CNC'd
surfaces do not
need finish, but
typically post
CNC since finish
is clear.
Clear is the most
common
Wet/Dip process most often applied
after CNC
E-coat
Cosmetic or
corrosion
protection
Wll provide a
semi-uniform
surface.
Thinness of
finish will show
as-cast surface
quality.
$ No Yes
Yes if CNC'd
surfaces do not
need finish
Black with little
control with our
current supply
base over the
color specs
Wet/Dip process most often applied
after CNC since masking for a dip
process is difficult. Finish is thin so
thermal impedance is minimal.
Wet process is difficult to mask.
No experience at AR with applying
before CNC and risk of scratching the
finish.
Anodize
Cosmetic and
Corrosion
protection
Can be applied
heavier than ecoat
to mask ascast
quality
$$ Not usually Yes
Yes if CNC'd
surfaces do not
need finish
Multiple, but
mroe $$$
Wet/Dip process most often applied
after CNC since masking for a dip
process is difficult. Finish is thin so
thermal impedance is minimal.
Wet process is difficult to mask.
No experience at AR with applying
before CNC and risk of scratching the
finish
Powder Coat
Cosmetic and
Corrosion
protection
Very good
cosmetics
$$ No Yes
Yes if CNC'd
surfaces do not
need finish
Multiple
Dry powder process.
Prototypes to date have shown that
powder coat is robust enough to be
applied before CNC machining
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 18 of 20
Process capabilities
As noted previously, die casting will yield a tighter tolerance as-cast part than the permanent mold process can achieve. If the part design can accommodate greater as-cast profile, linear and across parting line tolerance, precision can still be achieved where needed via CNC machining. While our supply base for high pressure die cast and permanent mold will provide tolerances based upon their capabilities which may be tighter than industry standards. However, if you can design to industry association published tolerances, you can create parts that are manufacturable regardless of supplier selection.
Example tolerances for HPDC and Perm Mold are included below. For a comprehensive tolerancing guide, is better to refer to industry standard data.
• Die Casting: The North American Die Casting Association (NADCA). NADCA Product Specification Standards for Die Castings 11th Edition 2021
• Permanent Mold: The Aluminum Association. Tolerances published as part of STANDARDS FOR ALUMINUM SAND & PERMANENT MOLD CASTINGS 16th Edition 2021; Engineering Series
General things to consider regarding tolerances:
• Linear tolerance is almost always considered as a % of unit length per unit length. For instance: Current NADCA dimensional tolerance is +/-0.25mm per 25mm, + additional 0.025mm per each full 25mm
• Tolerances across the parting line are always greater than on a single side of the tool. Projected part area may impact tolerance (more area=greater tolerance across parting line due to greater pressure)
• Tolerance to a moving core (slide or other side action): Similar to parting line tolerances, there is additional tolerance when considering dimensions that span from fixed steel to a moving core
Linear tolerance on one side of a mold example:
Perm Mold
Die Casting Standard Tolerance
Die Casting Precision Tolerance
Dimensions on one side of mold
Basic Tolerance up to 25mm
± 0.38mm
± 0.25mm
± 0.05
Additional Tolerance for each additional 25mm
± 0.051mm
± 0.025mm
± 0.025
Note regarding Standard vs Precision tolerances Normally, the higher the precision the more it costs to manufacture the part because die wear will affect more precise parts sooner. Production runs will be shorter to allow for increased die maintenance. Therefore the objective is to have as much tolerance as possible without affecting form, fit and function of the part.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 19 of 20
The geometry, feature and mold design cases for which tolerances are considered in the NADCA and Aluminum Org guidelines are extensive:
NADCA:
• Linear Dimensions Tolerances
• Parting Line Tolerances
• Moving Die Component Tolerances
• Angularity Tolerances
• Concentricity Tolerances
• Parting Line Shift
• Draft Tolerances
• Flatness Tolerances
Permanent Mold:
• Linear Dimensions Tolerances
• Parting Line Tolerances
• Side Core Tolerances
• Flatness Tolerances
• Profile Tolerances
Secondary operations
The majority of secondary operations which occur on castings is related to either part finishing (already discussed) or CNC machining where required for precision surfaces. CNC machining is an in-depth topic that will be covered in its own design guideline.
Other secondary operations on castings that are common at Amazon Robotics include:
• Tapping threads-completed as part of the CNC operation. Note that use of thread forming fasteners is an option that could eliminate pre-tapped holes to reduce cost.
• Press fit pins. We rely on our casting suppliers to press fit pins into place. The pin is included on the BOM and we use standard recommendations for hole diameter to specify in our data, but allow our suppliers latitude to CNC the dowel pin hole to their recommended diameter based upon their experiences
Cost drivers
Tooling costs. The following factors impact tooling cost and leadtime.
• As previously noted, High Pressure Die Cast Tooling will have higher costs and longer leadtime than a comparable mold for Gravity Cast/Permanent Mold.
• Mold and trim die complexity.
• Complex parting line, side action or slides-increased tooling cost and ongoing maintenance costs.
• Machining setups. Each machining setup will require a unique fixture.
Piece part cost. The following factors impact the piece part cost and leadtime.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00166 R01 AMAZON ROBOTICS CONFIDENTIAL Page 20 of 20
• Material: There may be differences in material cost for various alloys. This can be reviewed with a supplier. At the time of publishing the cost delta between die cast alloys A380 and AlSiFe(12) was negligible.
• Cycle time. As previously noted, High Pressure Die Cast Tooling will have lower as-cast piece part costs than a comparable part produced via Gravity Cast/Permanent Mold, due to shorter cycle times for die casting.
• Automation. Die cast presses and processes lend themselves to greater levels of automation which reduce labor costs.
• Part Size. Larger parts require more raw material. They may also have slower cycle times, which decreases machine utilization.
• Machining operations and total machining time.
• Finishing. See options above for relative cost impact. The finishing process selected plus any masking requirements will impact cost.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
P a g e | 1
300 Riverpark Drive, North Reading, MA 01864
1
Title: Process Guideline - Thermoplastic Injection Molding
DOCUMENT NUMBER: 930-00164
REVISION: 01
PROCESS OWNER: ADVANCED MANUFACTURING ENGINEERING
1. INTRODUCTION ..................................................................................................................................... 2
2. PROCESS OVERVIEW ............................................................................................................................. 2
2.1. INJECTION MOLDING EQUIPMENT ................................................................................................... 3
2.2. INJECTION MOLDS ............................................................................................................................ 3
2.3. TYPES OF GATES ................................................................................................................................ 9
2.4. TYPES OF INJECTION MOLDING PROCESS ....................................................................................... 15
3. SURFACE FINISHES .............................................................................................................................. 18
3.1. SANDING AND POLISHING .............................................................................................................. 18
3.2. EDM SPARK EROSION ...................................................................................................................... 19
3.3. MEDIA BLASTING ............................................................................................................................ 19
3.4. CHEMICAL PHOTOETCHING ............................................................................................................ 20
3.5. LASER ETCHING ............................................................................................................................... 20
4. PART DESING GUIDELINES .................................................................................................................. 21
4.1. PARTING LINE .................................................................................................................................. 21
4.2. UNDERCUTS .................................................................................................................................... 24
4.3. DRAFT ANGLE .................................................................................................................................. 24
4.4. RIBS, CORRUGATIONS AND GUSSETS ............................................................................................. 26
4.5. WALL THICKNESS ............................................................................................................................. 30
4.6. RADII AND CHAMFERS .................................................................................................................... 31
4.7. BOSSES ............................................................................................................................................ 33
4.8. DEFAULT SPECIFICATIONS FOR PLASTIC TOLERANCES ................................................................... 35
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 2 of 36
AMAZON ROBOTICS CONFIDENTIAL
1. INTRODUCTION
Injection Molding is the most common method for mass manufacturing of plastic products. Examples include automotive parts, packaging, toys, cases for electronics and a large variety of other parts.
This document will describe the different types of injection molding process, explore types of molds and their parts, explore surface finishes and provide guidelines for part design.
This document will not provide guidelines for tooling design, in regards to the cooling, ejection and venting systems or hydraulic or pneumatic mechanisms. This document will not cover complicated part design such as auto screwing molds, elbow molds or slides on lifter mechanisms.
2. PROCESS OVERVIEW
The injection molding process basically consists of compressing molten plastic into a mold, let it cool and remove it from the mold.
An injection molding machine, usually known as injection press, is divided in two fundamental units: the injection unit and the clamping unit. In the injection unit the solid plastic pellets are fed into the barrel of the injection unit through a hopper. Inside the barrel, a screw transports the pellets forward. Heaters wrapped around the barrel heat up the plastic material and as the pellets are moved forward by the screw, more heat is generated by the friction between the plastic and the screw and barrel causing the pellets to melt. Once enough molten plastic is in front of the screw it rams forward like a plunger of a syringe. In a matter of seconds, the screw injects the molten plastic from the injection unit into the clamping unit, inside an empty part of the mold, called the cavity. The plastic solidifies, usually in under a minute, the mold opens and the part is ejected. The mold then closes and the process repeats again.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 3 of 36
AMAZON ROBOTICS CONFIDENTIAL
2.1. INJECTION MOLDING EQUIPMENT
Hopper: It holds the material that will be processed
Barrel: It has a cylindrical shape and contains the screw that will plasticize the material
Screw: It conveys, plasticizes and is used to inject the molten material into the mold cavity through the nozzle
Heater Bands: It heats the barrel
Injection Cylinder: It pushes the screw in order to inject the molten material into the mold cavity
Nozzle: It is the channel through which the molten material is injected from the barrel, by the screw, into the mold cavity. Usually it contains a needle to avoid the material to return to the barrel
Check Valve: It prevents the molten material to return to the screw during the injection process
Fixed Platen: It is used to clamp the cavity side of the mold
Movable Platen: It is used to clamp the core side of the mold
Rear Platen: It is a fixed platen that supports the tie bars and clamping cylinder
Clamping Cylinder: It is the cylinder that will open and close the mold as well provide the clamping force to keep the mold closed during the injection process. It is also common to have a toggle mechanism to apply the clamping force
Ejection Cylinder: It drives the mechanisms that will eject the part from the mold
Tie Bars: It supports and keep the platens aligned
2.2. INJECTION MOLDS
An injection mold is a tool used to produce injection molded parts. It consists of a series of parts that allow the molten plastic material to be formed and cooled to create a desired component.
2.2.1. Mold Material
Injection molds are usually made of steel or aluminum. The choice of which material is used to build an injection mold depends on several factors, such as:
- Tooling cost - Advantage: It depends on which grade of steel or aluminum is chosen. Usually aluminum is cheaper than steel used for injection molds, but there are grades of steel that can be at the same price range of aluminum. One example is free machining steel, that is cheap and easy to machine. The overall value and return on investment of an aluminum mold and a steel mold can vary greatly, based on the usage of the mold (is it going to be a very high volume - millions of parts per year or is it going to be a low volume production rate - thousand or parts per year?), the intended production lifespan, material to be molded, etc. Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 4 of 36
AMAZON ROBOTICS CONFIDENTIAL
- Cost per part - Advantage: Toss-up. This factor depends on your intended production run, and the overall lifespan that you hope to get out of your part. For shorter runs, the lower upfront costs of aluminum molds can lead to lower overall cost per part. If you intend to use your mold for high volumes in the millions and tens of millions of parts, you’ll see the investment in a steel mold pay off. What’s more, the cost per part will decrease as you get a much longer service life. It’s critically important to plan how you’ll use your mold in advance, to get the greatest advantage in this area.
- Suitability for low volumes - Advantage: Aluminum. As mentioned above, aluminum molds will almost always offer better value for low-volume production runs — due to their lower upfront costs and ability to reliably produce parts into the thousands and tens of thousands of pieces. As always, review the specifics of your project to ensure that, for instance, aluminum is suitable for the material you’re using.
- Suitability for high volumes - Advantage: Steel. For molds intended for high volume and multiple production runs, a steel construction will typically be your better bet. Your higher upfront investment is rewarded with a piece of equipment that can reliably last for years with proper maintenance. The strength of steel is unparalleled for use in these types of longer production runs.
- Heating and cooling times - Advantage: Aluminum. With a much higher rate of heat dissipation than steel, aluminum molds can heat and cool much more quickly than steel molds — typically up to seven times. Cooling time, especially, makes up a significant portion of overall cycle time in injection molding. Thus, choosing an aluminum mold when appropriate can offer major benefits in cycle time which, in turn, means that you’re able to produce more parts more quickly.
- Suitability for advanced resins - Advantage: Steel. While both steel and aluminum are usually suitable for a broad range of standard injection molding resins, steel can offer an advantage if you’re working with more complex or advanced formulations — such as those reinforced with glass, fiber or other additives. A relatively softer metal like aluminum runs a greater risk of scratches or other damage from certain types of additives, which can affect the finish and texture of the final part.
- Shrink, warp and other defects - Advantage: Aluminum. The superior heat dissipation of aluminum means that the mold is better able to approach uniform heating and cooling times — and to do so more quickly — which provides an advantage in decreasing the number of defective and rejected parts. Non-uniform heating and cooling are among the biggest factors in defects such as sink marks, voids and burn marks. When used in the right application, aluminum molds can provide even better cost advantages due to lower rejection rates for parts.
- Ease of modification and repair - Advantage: Aluminum. Damaged or deformed steel molds can be difficult and costly to repair, depending on the hardness of the material. Sometimes, a new mold may be required in such cases. Aluminum molds are usually more receptive to repair and, as a softer material, can be more easily modified in cases where production errors may have occurred or design changes are required. One way to make future modifications easier is to use inserts for areas of high probability of changes, no matter what material is used to build the mold. In this case only the inserts will be replaced, making the whole modification process simpler.
- Suitability for detailed features - Advantage: Steel. When extremely fine, detailed features are required — such as those that push the boundaries of injection mold design best practices, e.g., thin, non-uniform walls, less rounded angles and tighter, narrower areas of the mold cavity — Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 5 of 36
AMAZON ROBOTICS CONFIDENTIAL
steel molds will often provide better results than aluminum. The strength and hardness of the steel means that it’s better able to hold a shape for those extremely high-precision areas.
- Durability - Advantage: Steel. The key benefit of steel molds is their vastly superior durability, over any other material available. When long production runs are expected, and the mold is intended for repeated use over many years, steel is the clear choice. The higher upfront investment required more than pays itself back over the repeated use and tens of millions of parts that the mold is capable of producing. Steel can also lower parts per cost far more than any other material allows. The flip side of this advantage is the risk of using an over-engineered solution for your application. Essentially, if you don’t require those long production runs and repeated uses, steel is less likely to prove a worthy investment.
-
2.2.2. Parts of an injection mold
This section describes the main components of an injection mold.
2.2.3. Types of Molds
The selection of the type of injection mold depends on the part geometry, part design requirements, tool design, production volumes and budget. The type of injection mold affects component quality and manufacturing cost. This section describes the various types of injection molds and their components.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 6 of 36
AMAZON ROBOTICS CONFIDENTIAL
- Mold Opening Mechanism
o Two Plate Mold
Two plate molds are the most commonly used type of injection mold. They consist of one parting plane where the mold splits. In a multiple cavity tool, runner and gate must be in the parting plane to ensure runner and gate ejection when mold opens.
o Three Plate Mold
Three plate molds consist of two parting planes and mold splits in three sections. Runner can be located on different parting lines, so they can be ejected separately, turning possible automatic degating.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 7 of 36
AMAZON ROBOTICS CONFIDENTIAL
- Feeding System
o Hot runner
Hot runner injection molds consist of a heated physical channel to direct molten plastic into the injection mold cavity. In this system, the runners are part of the injection mold. Temperature is kept above the material melting point.
o Cold runner
Cold runner injection molds consist of an unheated physical channel to direct molten plastic into the injection mold cavity after it leaves the nozzle. In this system, the runner is cooled and ejected every cycle with the part. After the complete injection cycle runner is removed from the molded part.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 8 of 36
AMAZON ROBOTICS CONFIDENTIAL
- Number of Cavities
o Single Cavity Mold
Single cavity mold produces only one part per cycle. The injection molding tool cost for a single cavity mold is low, but the unit part cost will be high. Single cavity molds are suitable for low production volumes.
o Multiple Cavity Mold
Multiple cavity mold produces more than one of the same part per cycle. Cavitation is the term used to describe the number of cavities an injection mold has. There are multiple factors to consider when determining how many cavities a mold should have. A mold with more cavities is more expensive than a mold with fewer cavities, due to its larger size and more complex hot runner system, if existing, but usually the part price is lower, because in one single cycle more parts are produced. Of course, this is not always the case, because depending on the size of the parts and the number of cavities, the mold can be very large, demanding a larger press with more clamping force and injection volume and it can make the process very expensive. Also, it is important to consider the demand of parts, making more sense to have more cavities for higher demand products. There is also an inherent risk of having one single large mold with many cavities, which is in case of damage to the mold or unplanned maintenance, the mold will be off production and it can disrupt the supply chain. So, there are multiple aspects when defining cavitation of injection molds and decision must be taken on a case-by-case basis.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 9 of 36
AMAZON ROBOTICS CONFIDENTIAL
o Family Mold
Family mold produces two or more parts per injection cycle. In this type of mold, different parts are molded in the same tool, usually parts that are used in the same product. The costs are lower than single mold cavity because with one mold more than one part can be molded. For example, if a product requires a top cover and a bottom cover and they are made of the same material with similar sizes and masses, family mold is an option to reduce costs.
Although family molds look like a good option to minimize initial investments, it is important to emphasize that there are some disadvantages as well. For example, if one of the parts is not usable, there will be an excess of the other part. There are also restrictions on the size and volume of the parts, which must be very similar. Any unbalance on weight and thickness will affect injection and cooling time, which may cause parts to warp or other defects. A Mold Flow analysis is highly recommended before proceeding with family tools.
2.3. TYPES OF GATES
A critical component in mold design is choosing the correct gate. The function of the gate is a simple concept, but choosing the wrong type of gating can cause several problems during processing. This section will describe the several different kinds of gate designs and how they are used.
There are important factors to consider when choosing the gate type/location for a molded part. The first is how the mold will be designed and where a gate can be located. Part orientation in the mold, show surface location, and action locations can limit the options for gating. Further design considerations are material selection, part volume/size and production functionality.
Some plastics are more sensitive to over-heating conditions. This is known as shear heating. Any time plastic is forced through a restricted area, there is some amount of shear heating. Attempting to fill a large plastic part with a small gate will create excessive shear heating and could degrade the plastic. For example, gate designs like submarine gates have limitations to the maximum size of the gate, which may eliminate the gate design as a possibility for larger parts.
Gate freeze is an important aspect of the injection molding process. Generally speaking, gates need to be large enough to fill out the cavity properly but small enough to seal the cavity (gate freeze). Gate Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 10 of 36
AMAZON ROBOTICS CONFIDENTIAL
freeze should occur when the cavity is completely packed out and ready to start the cooling process. Since the gate is small, it should cool off relatively quickly compared to the molded part or the feed system. Gate freeze allows the part to become isolated from the feed system and for the injection molding machine to move onto the cooling/charging phase of the molding process.
The function of the mold in the production environment is another consideration. A defining characteristic of the different kinds of gates is whether they break from the molded part automatically or require trimming. In higher volume applications, it becomes less feasible for an operator to trim gates manually. In this case, either factoring in robotic gate cutting (Nipping) or changing gate designs should be factored in. Scrap costs generated from cold runner systems may justify a hot runner where zero scrap is generated.
The most common gates types in injection molding are:
- Manually trimmed
o Sprue gate - this gate is suitable for single chamber parts and thick sections because it can hold pressure well. The disadvantage of this gate is that a mark is left on top.
o Edge or side gate - this is commonly used for molds that have two or more cavities. It is placed at the side of the molds and the gate is done manually by a cutter
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 11 of 36
AMAZON ROBOTICS CONFIDENTIAL
o Tab gate - this is another common gate style that contains an auxiliary tab section where shear stress can safely be absorbed without affecting the quality of the part. It is suitable for thin and flat parts
o Overlap gate - this gate is similar to an edge gate, except the gate overlaps the wall or surfaces. This type of gate is typically used to eliminate jetting.
o Film or flash gate - this gate consists of a straight runner and a gate land across either the entire length or a portion of the cavity. It is used for long flat thin walled parts and provides even filling.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 12 of 36
AMAZON ROBOTICS CONFIDENTIAL
o Diaphragm gate - this gate is often used for gating cylindrical or round parts that have an open inside diameter. It is used for single cavity molds that have a small to medium internal diameter. It is used when concentricity is important and the presence of a weld line is not acceptable or when an even plastic flow is desired. Having even plastic flow helps to ensure that, when cooling, the part shrinks as consistently as possible and reduces stress on the molded part.
o External ring - this gate is used for cylindrical or round parts in a multiple cavity mold or when a diaphragm gate is not practical. Material enters the external ring from one side forming a weld line on the opposite side of the runner this weld line is not typically transferred to the part.
o Internal ring gate - this gate is used for cylindrical or round parts in a multiple cavity mold or when a diaphragm gate is not practical. Material enters the ring from inside forming a weld line on the opposite side of the runner this weld line is not typically transferred to the part.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 13 of 36
AMAZON ROBOTICS CONFIDENTIAL
- Automatically trimmed
o Pin gate - this gate is only feasible with a 3-plate tool because it must be ejected separately from the part in the opposite direction. The gate must be weak enough to break off without damaging the part. This type of gate is most suitable for use with thin sections.
o Submarine (tunnel) gate - this gate is used in two-plate mold construction. An angled, tapered tunnel is machined from the end of the runner to the cavity, just below the parting line. As the parts and runners are ejected, the gate is sheared at the part. The tunnel can be located either in the moving half or in the fixed half. A sub-gate is often located into the side of an ejector pin on the non-visible side of the part when appearance is important.
o Cashew gate - this is a variation of the tunnel gate design and consists of a curved tunnel gate where the tunnel is machined in the movable mold half.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 14 of 36
AMAZON ROBOTICS CONFIDENTIAL
o Hot runner gate - this gate is also known as sprueless gate. It is used to deliver hot material through hot runners into the cavity. The nozzle of a runnerless mold is extended forward to the part and the material is injected through a pinpoint gate. The face of the nozzle is part of the cavity surface; this can cause appearance issues (matte appearance and rippled surface). The nozzle diameter should be as small as possible. Most suitable for thin walled parts with short cycle times, this avoid freezing of the nozzle.
o Valve gate - this gate adds a valve rod to the hot runner gate. The valve can be activated to close the gate just before the material near the gate freezes. This allows a larger gate diameter and smooths the gate scar. Since the valve rod controls the packing cycle, better control of the packing cycle is maintained with more consistent quality.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 15 of 36
AMAZON ROBOTICS CONFIDENTIAL
2.4. TYPES OF INJECTION MOLDING PROCESS
2.4.1. Gas Assisted Injection Molding
Gas assisted injection molding consists of a process that introduces nitrogen gas into a mold cavity after it has been partially filled with plastic up to 70-80% of the mold volume. The compressed nitrogen displaces a portion of the molten plastic when injected into the cavity. The result is hollow parts that are light and relatively inexpensive to make. Designers can use gas-assist molding to create thin-walled parts. Such parts can be molded with low clamp tonnage, which reduces both tooling cost and required injection molding machine size.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 16 of 36
AMAZON ROBOTICS CONFIDENTIAL
2.4.2. Over Molding & Insert Molding
Over molding is an injection molding process used to mold one plastic (commonly a rubber-like plastic such as TPE) over top of another part (substrate). The substrate is usually an injection molded plastic part, but various other materials could also be used. Sometimes this process is also called insert molding, especially when the substrate is a metallic part.
Over molding process can be used to combine two parts of different materials in one single part, eliminating one step of the assembly process. It can provide two-tone aesthetics to parts, or add molded sealing or gaskets to the final part, or add a grip area to handles, for example.
In the case of insert molding, when the substrate is a metallic part, the insert is assembled to the mold prior to the injection process and the molten material is molded on top of it.
2.4.3. Film Insert Molding
Film Insert Molding consists of a process that molds the plastic material on top of a plastic film, usually decorated by printing on the back. This film can be flat or pre-shaped to the required design, depending on the application.
This process is also knows as In-Mold Decorating (IMD) or In-Mold Label (IML), depending on some characteristics. Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 17 of 36
AMAZON ROBOTICS CONFIDENTIAL
2.4.4. Double Injection Molding
Double Injection, sometimes known as 2 material 2 shot molding, is a manufacturing process used to produce complicated molded parts from two different materials. Through a highly specialized and automated process, two different materials, including two different resins (since compatible) can be molded into a single, multi-chambered mold.
Double Injection is performed on one machine that is programmed to perform two injection shots in one cycle. In the first shot, a nozzle injects plastic into a mold. The mold is then automatically rotated and a different type of plastic is injected into the mold from a second nozzle.
Double Injection Molding leverages the compatibility between materials to create molecular bond. The result is a single part with production and feature advantages. It can be used for a variety of product designs across all industries. It also allows for molding using clear plastics, colored graphics and stylish finishes which improves your product functionality and marketplace value.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 18 of 36
AMAZON ROBOTICS CONFIDENTIAL
3. SURFACE FINISHES
After rough machining there are always tool marks left on the mold surface. If these marks remain untreated, they would get transferred to the part during molding. Surface finishing requirements usually depend on the part application, but even within the same part, there might be different requirements for different locations or sides. For instance, parts or portions of the parts may be non-visible or non-aesthetic, other parts or portions of the parts may require high gloss or a specific texture. So different surface finishing treatments are necessary to meet those requirements.
It is also important to mention that depending on the machining method, more or less polishing or finishing will be necessary. For example, rough machining leaves much more marks than finish machining. If wire EDM (Electrical Discharge Machining) milling is used, it is very likely that polishing or finishing will not be needed because of the nature of this process that produces a very smooth surface on the tool.
Surface finishes, such as textures, are also an effective way of hiding molding defects. For example, if there is an aesthetic area that contains a wall on the other surface and therefore is susceptible to sinking, a texture can be added so it will help hiding potential sink marks.
There are several surface finish options for injection molded plastic parts. Surface finishing procedures for injection molding can help to either increase or decrease the roughness of a part. Plastic glossy texture may be preferred for aesthetic parts, while rougher finishes may be best for certain mechanical parts or to reduce overall costs. It is also possible to create special textures, depending on the application.
3.1. SANDING AND POLISHING
There are twelve grades of finishes specified by the Plastics Industry Association (PLASTICS, former SPI) in four categories that range from shiny to dull. Each grade has different requirements for allowable deviation from perfect, with lower numbers allowing for less deviation and higher numbers allowing for more deviation.
Finishing Standard
Surface Roughness Ra (μm)
Finishing Method
Finishing Look
A-1
0.012 to 0.025
6000 Grit Diamond
Super High Glossy finish
A-2
0.012 to 0.025
3000 Grit Diamond
High Glossy finish
A-3
0.05 to 0.10
1200 Grit Diamond
Normal Glossy finish
B-1
0.05 to 0.10
600 Grit Paper
Fine Semi-glossy finish
B-2
0.10 to 0.15
400 Grit Paper
Medium Semi-glossy finish
B-3
0.28 to 0.32
320 Grit Paper
Normal Semi-glossy finish
C-1
0.35 to 0.40
600 Grit Stone
Fine Matte finish
C-2
0.45 to 0.55
400 Grit Stone
Medium Matte finish
C-3
0.63 to 0.70
320 Grit Stone
Normal Matte finish
D-1
0.80 to 1.00
Dry Blast Glass Bead
Satin Textured finish
D-2
1.00 to 2.80
Dry Blast #240 Oxide
Dull Textured finish
D-3
3.20 to 18.0
Dry Blast #24 Oxide
Rough Textured finish
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 19 of 36
AMAZON ROBOTICS CONFIDENTIAL
3.2. EDM SPARK EROSION
Electrical Discharge Machining erosion uses a graphite or copper electrode placed in an electrolytic bath of water or oil. The electrode discharges a spark that strikes the tool wall. This process is ideal for making deep thin slots, sharp concave corner and other features. A very fine and smooth finish can be achieved, which would be time-consuming and expensive if done manually.
3.3. MEDIA BLASTING
In this process, high pressure air is used to spray various types of dry or wet abrasive media against the tool wall. Examples of these media would be silica (sand), aluminum oxide, glass or plastic beads. This method is commonly used to clean the tool and at the same time create a uniform matte or satin finish.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 20 of 36
AMAZON ROBOTICS CONFIDENTIAL
3.4. CHEMICAL PHOTOETCHING
In this process, the tool wall is coated with a photoresist or light sensitive chemical. The desired pattern is optically projected onto the tool surface and any areas struck by UV light are cured. The remaining photoresist get washed away, leaving behind a film mask. The mold is then bathed in acid, which etches away the unprotected areas and creates the desired texture.
This is a great method to create sophisticated in-molded patterns and textures. It can imitate the look of leather, stone, wood grain or even abstract geometric designs.
3.5. LASER ETCHING
This process allows to create almost any texture on any surface due to its flexibility. Usually robotic arm with 6 axes of movement is used to apply the laser accurately on the mold surface. It can also reach undercuts and other hidden areas. This method is most often used in large parts, such as automotive dashboards, which have fine patterns that are consistent over a long length. Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 21 of 36
AMAZON ROBOTICS CONFIDENTIAL
4. PART DESING GUIDELINES
This section describes important design characteristics that need to be considered when designing a plastic part for injection molding. It also contains a table with basic specifications for plastics tolerances.
4.1. PARTING LINE
Parting line is an inevitable part of injection molded products. It is the line of separation between where two halves of a mold meet and it runs the entire perimeter of the part. It is also where a slide mechanism might meet where it shuts off on one of the mold halves. The parting line will always be visible, but can be minimized by its location, draft allowance and part geometry.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 22 of 36
AMAZON ROBOTICS CONFIDENTIAL
There are 5 types of parting lines:
- Vertical parting lines - this is the most common type of parting line. It is a plane perpendicular to the mold opening direction.
- Stepped parting line - depending on the part geometry, the parting line can be stepped. In this case, an unbalanced force is generated on both sides of the cavity, which can cause the halves of the mold to slide. This can be overcome using pins to support the force.
It is also possible to eliminate the unbalancing with a symmetrical arrangement of the cavities.
- Beveled parting lines - this is similar to stepped parting line, but with a beveled shape
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 23 of 36
AMAZON ROBOTICS CONFIDENTIAL
- Curved parting lines - this is similar to stepped parting line, but with a curved shape
- Comprehensive parting lines - this form is designed based on the structure of the plastic part, it can combine all other parting line forms.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 24 of 36
AMAZON ROBOTICS CONFIDENTIAL
4.2. UNDERCUTS
During the design phase of an injection molded part it is important to consider that the plastic goes into the mold as liquid it cools rapidly and solidifies into the shape of the cavity. Designing a part that can be ejected using a “straight pull” is key to keeping the cost of the injection mold down. A straight pull mold is designed so that when the two halves separate from each other, there is no metal blocking the path of the plastic in the direction of the pull. If the part requires a snap-fit, a hole or any detail on the sides of the part, mold will require slides and lifter mechanisms to allow the part to be ejected.
Avoiding undercuts might be the best option. Undercuts always add cost, complexity, and maintenance requirements to the mold. A clever redesign can often eliminate undercuts.
4.3. DRAFT ANGLE
A draft angle is the amount of taper that is applied to each side of most features of an injection molded part. The angle, which is positioned to run toward the direction of a mold’s pull and parting line, helps with releasing the part from the mold. Most of the times draft is required to allow a successful ejection of the molded part. There are a very few cases where draft may not be needed, such as low-friction materials or special features like crush ribs.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 25 of 36
AMAZON ROBOTICS CONFIDENTIAL
Having draft is crucial to manufacturing parts that meet quality standards. Without draft, major problems can arise in the injection molding process that increase the time and cost of production.
When no draft is designed into the part, problems can come from friction and vacuums. These issues can damage both the part and even the mold in extreme cases. These problems are a direct result of having insufficient draft. Because plastic shrinks as it cools, portions of the part may pull away from the mold while others grip the core. If there is no draft angle that allows a simple push from the ejector pins to pop the part out of the mold, the part’s surfaces will often drag along the mold as it is being ejected. This friction between the two surfaces can cause scratches or gouges in the part and affect the appearance. This is particularly troublesome if your part is being molded with a surface finish or texture. The friction will scrape away texture and leave you with many rejected parts.
The recommended draft angle depends on many factors:
- Material shrinkage - some materials shrink more than others. In general, the higher the shrinkage, the larger the draft angle needed to prevent ejection issues.
- Height and shape of wall or feature - a shallow single straight rib having not enough draft causes less problems than a high cylindrical wall.
- Surface texture - a polished surface requires a smaller draft angle than a surface that is textured.
- Aesthetic requirements - scuff marks might not be as big of a problem on a technical part "hidden" in an assembly while, for the cover part of the assembly, they may be totally unacceptable.
The figure below shows a guideline for draft angles, considering all the above factors:
- Typically, one to three degrees draft is recommended.
- For untextured surfaces, generally a minimum of 0.5 degree is recommended.
- For textured surfaces on sidewall, an additional 0.4-0.5 degree is recommended per 0.1mm of texture depth.
Draft in mm for various draft angles as function of depth
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 26 of 36
AMAZON ROBOTICS CONFIDENTIAL
4.3.1. Draft Angle for Shut-offs
The most straightforward mold construction is where the parting plane of the mold halves is a flat surface perpendicular to the draw direction. This setup also offers the easiest way to make sure that there is no gap between the mold halves when they are closed. After all, the clamping force of the injection molding machine acts perpendicular to the parting plane. However, it is not always possible or even beneficial to keep the parting plane flat.
In case of such a stepped parting line, the parting line jumps from one level to another. The surface needed to bridge these levels is called a shut-off because it is where the mold halves shut against each other. The shut-off should never be exactly parallel to the draw direction. This leads to drag, causing the tool to wear over time. In a worst case scenario, misalignment during mold closing can cause significant damage. Instead, draft should be applied to guarantee proper shut-off.
On stepped parting surfaces, a draft of seven or more degrees is always recommended. Five degrees should be considered as a minimum.
4.4. RIBS, CORRUGATIONS AND GUSSETS
When the stiffness of a plastic part needs to be improved, it is necessary to either increase its sectional properties or change the material. Sometimes, it may be enough to change the material grade, for example using a higher glass fiber content. If that is not sufficient or desired for other reasons, increasing the sectional properties is often the solution.
In many cases, the simplest way to improve the sectional properties is increasing wall thickness. However, this has some limitations. Additional reinforcement can be obtained by adding corrugations or placing ribs perpendicular to the parts wall. Adding corrugations typically has a smaller impact on part weight and cooling time, but adding ribs has a bigger potential in terms of increasing the stiffness. Ribs allow for the facing or mating surface of a part to be smooth, which can be beneficial for aesthetic or functional reasons. Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 27 of 36
AMAZON ROBOTICS CONFIDENTIAL
4.4.1. Ribs
Rib dimensioning
When adding ribs, the following guidelines for dimensioning should be applied:
− The thickness of the rib should be approximately 50 to 60% of the general wall thickness of the part. Exceeding this value may lead to sink marks on the surface opposite the ribs. It can negatively influence material flow during injection, possibly resulting in weld lines and voids.
− The rib height should not exceed three times the general wall thickness as deep ribs become difficult to fill and may stick in the mold during ejection.
− On the sides of ribs, a draft angle of 1 - 1.5 degree should be applied. This means that the ribs are slightly tapered, becoming slightly thinner towards the top. This makes ejection of the part from the mold easier. On low ribs and in exceptional cases, a smaller or even no draft angle is acceptable. It should be noted though, that this may lead to cosmetic defects like scuff marks or issues with ejecting the part after molding.
− At the base of the rib, where it intersects with the nominal wall, a radius of 25 - 50% of the general wall thickness should be included. A minimum radius of 0.4 mm is suggested. This will eliminate a potential stress concentration and improve flow and cooling characteristics around the rib. When exceeding the 50% value, a material mass develops, increasing the risk of molded-in residual stresses, voids or sink marks.
− Spacing between two parallel ribs should be at least two times the general wall thickness. This prevents the mold from developing a hot blade that is fragile and has cooling problems.
Rib placement
When placing ribs, the following guidelines for placement should be applied:
− Ribs are preferably designed parallel to the melt flow as flow across ribs can result in a branched flow leading to trapped gas or hesitation. Hesitation can increase internal stresses and short shots.
− Parallel ribs should be spaced at a minimum distance of twice the nominal wall thickness; this helps prevent cooling problems and the use of thin blades in the mold construction. Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 28 of 36
AMAZON ROBOTICS CONFIDENTIAL
− Ribs should be orientated along the axis of bending in order to provide maximum stiffness. Consider the example below, where a long thin plate is simply supported at the ends. If ribs are added in the length direction, the plate is significantly stiffened. However, if ribs are added across the width of the plate, little improvement is found.
− When adding ribs to a profile or boxed section, their placement and orientation has a large impact on the obtained additional stiffness.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 29 of 36
AMAZON ROBOTICS CONFIDENTIAL
− For maximum performance and function, the neutral lines of the ribs and profile wall should meet at the same point. However, depending on the specific dimensions and material of choice, sink marks may occur. This can be avoided but will result in a weaker geometry:
o If the diagonal ribs are moved slightly apart, the rigidity is reduced 35%.
o If a short vertical rib is added to the design, the torsional rigidity is reduced an additional 5%
4.4.2. Gussets
Gussets can be used to reinforce corners, side walls and bosses. They can be considered as a subset of ribs, meaning that the guidelines for rib dimensioning and placement are also valid for gussets.
4.4.3. Corrugations
Adding corrugations to the design can stiffen flat surfaces in the direction of the corrugations. They are very efficient and do not add large amounts of extra material or lengthen the cooling time. The extra stiffness is a result of increasing the average distance of the material from the neutral axis of the part.
In order to increase stiffness in the direction perpendicular to the corrugations and improve straightness, walls can be added and the corrugation profile can be offset by about half the corrugation Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 30 of 36
AMAZON ROBOTICS CONFIDENTIAL
pitch. The distance between the wall will depend on the material and thickness of the part and should be determined case by case.
4.5. WALL THICKNESS
The recommended general wall thickness of injection molded parts depends on the size of the geometry, the material of choice and the desired performance of the geometry.
Typically, the recommended wall thickness is in the range 0.5 mm to 4 mm. In specific cases, wall thicknesses can be either smaller or bigger. A basic design guideline is to keep wall thicknesses as thin and as uniform as possible. Where varying wall thicknesses are unavoidable for reasons of design, there should be a gradual transition as indicated below:
The wall thickness is important because of its influence on:
− Mold filling - if the wall thickness doesn’t fit the flow behavior of the thermoplastic material, it may be hard to completely fill the mold.
− Part weight - the greater the wall thickness, the heavier the part.
− Cooling time - the greater the wall thickness, the longer it will take for the part to cool down after injection molding. Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 31 of 36
AMAZON ROBOTICS CONFIDENTIAL
− Part cost - both of the above, plus larger part volume and increased injection molding cycle time results in higher part cost.
− Dimensional accuracy - different areas of the part having different cooling rates, which is typically the case when the wall thickness is high or not uniform, leads to molded-in residual stresses that cause the part to warp after being ejected from the mold.
− Part performance - thick sections can cause voids to arise within the wall thickness.
− Part aesthetics - If the wall thickness is too high, non-uniform cooling rates may lead to sink marks.
4.6. RADII AND CHAMFERS
Sharp edges and corners should always be avoided. This is because they lead to the following results:
− High molded-in stresses
− Poor flow characteristics
− Reduced mechanical properties
− Increased tool wear
− Surface appearance problems
Instead, by applying radii and fillets, the following results can be achieved:
− Less warpage
− Less flow resistance and easier filling
− Reduced stress concentration
− Less notch sensitivity
− More uniform cooling
− Better appearance
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 32 of 36
AMAZON ROBOTICS CONFIDENTIAL
For radii and fillets, these are the recommended guidelines:
− Sharp corners should be rounded with a radius measuring between 25% and 60% of the nominal wall thickness, depending on the case.
− A minimum inner corner radius of 0.5 mm is suggested.
− In order to keep the wall thickness uniform, the outside radius of a corner should be equal to the inner radius plus the wall thickness.
− All sharp outer part and rib edges should be broken with at least a 0.125 mm radius.
− For a part with an inner corner radius half the nominal wall thickness, a stress concentration factor of 1.5 is a reasonable assumption. For smaller radii, for example 10% of the nominal wall, this factor will increase to 3. Standard tables for stress concentration factors are available and should be consulted for critical applications.
Like a radius or fillet, a chamfer can be used to soften sharp edges or make a gradual transition between two perpendicular faces. In view of minimizing stress concentration and optimizing flow, a radius is better than a chamfer. However, a chamfer can offer additional functionality like facilitating manual positioning of parts during assembly. A chamfer can also be used from an aesthetics point of view: where many parts are rounded-off, a chamfered edge creates a distinctive look. As with radii, a uniform wall thickness is preferred, so a chamfer on an outer edge should be copied on the inner corner.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 33 of 36
AMAZON ROBOTICS CONFIDENTIAL
4.7. BOSSES
A boss is a cylindrical protrusion placed on a part’s wall. A boss can have various functions, such as the following:
− Positioning aid - To help align parts during assembly; for example, a pin on one part will fit a hole in the other part.
− Fixation point - In the example mentioned above, the pin and hole can have a press fit. Friction between the two keeps the parts fixed. A boss can also be a tubular protrusion that can accommodate self-tapping screws to fix other parts.
− Bearing surface - A cylindrical protrusion can act as a bearing for another part; for example, a lever or a gear to rotate about.
The dimensions of a boss depend on its function. Manufacturability and aesthetics should be considered, for example, thick sections need to be avoided as these can lead to an increased injection molding cycle time, non-uniform shrinkage, sink marks and molded-in stresses. If the boss is to be used to accommodate self-tapping screws or inserts, the wall section must be controlled to avoid excessive stress in the boss.
General recommendations regarding boss dimensions include the following:
− The wall thickness of a boss should be less than 50% of the general wall thickness.
− A radius of 25% of the general wall thickness or 0.4 mm should be applied at the base of the boss to avoid stress concentration.
− A minimum draft of 0.5 degrees is required on the outer surface of the boss to facilitate release from the mold on ejection.
− In case of a tubular boss, the risk of sink marks can be reduced by extending the core pin so that it slightly penetrates the wall the boss is placed on. A minimum radius of 0.25 mm should be applied to the edge of the core pin to reduce material turbulence during filling and to help keep stresses to a minimum. Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 34 of 36
AMAZON ROBOTICS CONFIDENTIAL
− A minimum draft of 0.25 degrees is required on the inner surface of a tubular boss for ejection and or proper engagement with a fastener.
The strength of a boss can be increased by adding gussets or by connecting it to a sidewall by adding a rib. In that case:
− Bosses adjacent to external walls should be positioned a minimum of 3 mm from the surface to avoid local material accumulation.
− Regarding spacing between bosses, a minimum distance of twice the nominal wall thickness should be used.
Note: For cases like this, where steel features will be exposed to bending forces, it is recommended a maximum aspect ratio of 3:1 (height:width) to avoid stress during the fill cycle and tension cycling during the eject cycle. For higher ratios it is also recommended that these features should be aligned with the flow direction of the molten polymer.
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 35 of 36
AMAZON ROBOTICS CONFIDENTIAL
4.8. DEFAULT SPECIFICATIONS FOR PLASTIC TOLERANCES
Feature Size
0-10
mm
10.1-25 mm
25.1-50 mm
50.1-75 mm
75.1-100 mm
100.1-150 mm Toolbound Commercial Tol (mm) +/- 0.100 +/- 0.125 +/- 0.150 +/- 0.200 +/- 0.225 +/- 0.250
Toolbound Fine Tol (mm)
+/- 0.050
+/- 0.075
+/- 0.100
+/- 0.125
+/- 0.150
+/- 0.175 Non-Toolbound Commercial Tol (mm) +/- 0.200 +/- 0.225 +/- 0.250 +/- 0.300 +/- 0.350 +/- 0.400
Non-Toolbound Fine Tol (mm)
+/- 0.100
+/- 0.125
+/- 0.150
+/- 0.175
+/- 0.200
+/- 0.225
Feature Size
150.1-200 mm
200.1-250 mm
250.1-300 mm
300.1-350 mm
350.1-400 mm
400.1-450 mm Toolbound Commercial Tol (mm) +/- 0.500 +/- 0.650 +/- 0.800 +/- 0950 +/- 1.100 +/- 1.250
Toolbound Fine Tol (mm)
+/- 0.275
+/- 0.375
+/- 0.475
+/- 0.575
+/- 0.675
+/- 0.775 Non-Toolbound Commercial Tol (mm) +/- 0.600 +/- 0.750 +/- 0.900 +/- 1.050 +/- 1.200 +/- 1.350
Non-Toolbound Fine Tol (mm)
+/- 0.325
+/- 0.425
+/- 0.525
+/- 0.625
+/- 0.725
+/- 0.825
Toolbound: Dimensions that are contained in a single side of the tool, within in a single or non-moving piece of the tool
Non-Toolbound: Dimensions that are across moving sections of the tool, including: parting line, lifter, slide, cavity to core Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
930-00164 R01 Page 36 of 36
AMAZON ROBOTICS CONFIDENTIAL
REVISION HISTORY
Rev.
ECO #
Description of Change
Sections Affected
Originator/Department
01
DECO-03653
Initial Release
All
Gustavo Frattini / AME
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0
AR SHEET METAL DESIGN
BEST PRACTICES
930-00172_R01
Hardware Engineering
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-28 14:43:23.0
WELDING FUNDAMENTALS
&
AWS BASICS
Prepared by Marc-Andre Gouin, P. Eng.
(C): +1-514-234-4673;
@: mgouin@cmp-ams.com
Revision 01 Released to PROTOTYPE Lifecycle on 2022-01-26 21:17:47.0