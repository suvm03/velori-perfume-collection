# VELORI design collection

60-page master catalogue and 24-page technical drawing book. All artwork is original vector concept visualisation, not photorealistic 3D rendering. Blender was unavailable in the execution environment.

Individual_Bottle_Designs contains eight 2400-3000 px PNGs per design, editable SVGs, label artwork and JSON/text specifications. Packaging_Concepts contains 24 retail mockups, conceptual carton artwork PDFs/SVGs, gift and display/campaign images.

## Rebuild
Use Python 3.11+ with PyMuPDF and Pillow installed. Run `python Source_Files/build_all.py` from any directory to rebuild and verify all deliverables. Edit the rows, shapes and collection metadata in the script to change designs; concepts.json records the generated specifications. The build uses the Arial font convention for SVG artwork; the Python/Pillow imports support verification assets. No Blender dependency is required.

## Production status
Dimensions and capacities are preliminary. Technical drawings show overall envelopes, not production sections, tolerances or engineered closures. Young-user cap-open views depict exposed applicators; retained hinges remain an engineering proposal. Carton PDFs are conceptual RGB artwork, not approved press files: supplier must create a validated dieline with proper flap geometry, glue allowances, bleed, CMYK profile and barcode/label copy. Brand clearance, formula development, age-specific safety assessment, physical tests and destination-market review remain required. No production-ready or child-safety certification is implied.

## Regulatory references
FDA: https://www.fda.gov/cosmetics/resources-industry-cosmetics/small-businesses-homemade-cosmetics-fact-sheet
European Commission: https://single-market-economy.ec.europa.eu/sectors/cosmetics/scientific-and-technical-assessment_en
European Commission allergens: https://single-market-economy.ec.europa.eu/sectors/cosmetics/cosmetic-products-specific-topics/fragrance-allergens-labelling_en
Reviewed 02 October 2026. These are selected US/EU references, not worldwide compliance clearance.
