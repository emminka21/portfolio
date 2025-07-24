#!/usr/bin/env python3
"""
Script pro převod PDF portfolia na webové obrázky
"""

import os
import fitz  # PyMuPDF
from pathlib import Path
from PIL import Image
import io

def convert_pdf_to_images(pdf_path, output_dir):
    """Převede PDF na obrázky pomocí PyMuPDF"""
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF soubor nenalezen: {pdf_path}")
        return False
    
    # Vytvoř výstupní složku
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"🔄 Převádím PDF: {pdf_path}")
    print(f"📂 Výstup do: {output_dir}")
    
    try:
        # Otevři PDF
        print("⏳ Načítám PDF...")
        doc = fitz.open(pdf_path)
        
        print(f"✅ Nalezeno {doc.page_count} stránek")
        
        # Převeď každou stránku
        for page_num in range(doc.page_count):
            page = doc[page_num]
            
            # Vytvoř obrázek s vysokým rozlišením
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom pro lepší kvalitu
            pix = page.get_pixmap(matrix=mat)
            
            # Převeď na PIL Image
            img_data = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))
            
            # Optimalizuj velikost pro web
            if img.width > 1200:
                ratio = 1200 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((1200, new_height), Image.Resampling.LANCZOS)
            
            # Ulož jako JPEG
            filename = f"page_{page_num + 1:02d}.jpg"
            filepath = os.path.join(output_dir, filename)
            img.convert('RGB').save(filepath, 'JPEG', quality=85, optimize=True)
            
            print(f"💾 Uloženo: {filename} ({img.width}x{img.height})")
        
        doc.close()
        print(f"🎉 HOTOVO! Převedeno {doc.page_count} stránek")
        return True
        
    except Exception as e:
        print(f"❌ Chyba při převodu: {e}")
        return False

def main():
    """Hlavní funkce"""
    print("🚀 PŘEVOD PDF PORTFOLIA NA OBRÁZKY")
    print("=" * 40)
    
    pdf_file = "portfolio.pdf"
    images_dir = "images"
    
    success = convert_pdf_to_images(pdf_file, images_dir)
    
    if success:
        print("\n✅ ÚSPĚCH!")
        print(f"📁 Obrázky jsou ve složce: {images_dir}/")
        print("🌐 Teď můžu aktualizovat web s tvými skutečnými pracemi!")
    else:
        print("\n❌ NEÚSPĚCH!")
        print("Zkontroluj, že je PDF soubor na správném místě.")

if __name__ == "__main__":
    main()
