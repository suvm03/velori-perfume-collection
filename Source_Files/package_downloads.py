"""Refresh the complete collection archive without regenerating web images."""
from pathlib import Path
import zipfile

def refresh_complete_archive():
    root=Path(__file__).resolve().parents[1]
    with zipfile.ZipFile(root/'downloads/VELORI_Complete_Collection.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for name in ['Individual_Bottle_Designs','Packaging_Concepts','Source_Files','assets','.github']:
            for p in sorted((root/name).rglob('*')):
                if p.is_file() and '__pycache__' not in p.parts:archive.write(p,p.relative_to(root))
        for name in ['Perfume_Collection_Master_Catalogue.pdf','Technical_Drawings.pdf','README.md','WEBSITE_README.md','index.html','styles.css','styles-3d.css','app.js','viewer-3d.js','.nojekyll','Quality_Checks/Verification_Report.json','Quality_Checks/Website_Verification.json']:
            p=root/name
            if p.is_file():archive.write(p,name)
        for p in sorted((root/'downloads').glob('V[0-9][0-9]_Design_Pack.zip')):archive.write(p,p.relative_to(root))
    print('Complete collection archive refreshed.')

if __name__=='__main__':refresh_complete_archive()
