import os
import sys
import zipfile
import patoolib
import simple_colors

CALL_SCRIPT_ERROR   = "INVALID SCRIPT CALL! PLEASE CALL SCRIPT WITH -- python{3} python-zipfiles.py [input_path] [output_path] [zip/unzip]"

def unzip(pathIN, pathOUT="."):
    
    if not os.path.isdir(pathOUT):
        try:
            os.mkdir(pathOUT)
            print("Output directory created")
        except Exception as e:
            print(simple_colors.red(f"Error while creating directory: {str(e)}"))
            return
    
    try:
        patoolib.list_archive(archive=pathIN)
        patoolib.extract_archive(archive=pathIN, outdir=pathOUT)
        print(simple_colors.green(f"Unzipped files from {pathIN} to {pathOUT}"))
    except Exception as e:
        print(simple_colors.red(f"Error while unzipping: {str(e)}"))

def zip(pathIN, pathOUT="."):
    try:
        with zipfile.ZipFile(pathOUT, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isdir(pathIN):
                counter = 0
                for dir, _, files in os.walk(pathIN):
                    for file in files:
                        print("Zipping file: " + os.path.join(dir, file))
                        zipf.write(os.path.join(dir, file), os.path.relpath(os.path.join(dir, file), pathIN))
                        counter += 1
            else:
                zipf.write(pathIN, pathIN)
                counter = 1
        print(simple_colors.green(f"Zipped files from {pathIN} to {pathOUT} | Total zipped: " + str(counter)))
    except Exception as e:
        print(simple_colors.red(f"Error while zipping: {str(e)}"))

def main():
    
    if len(sys.argv) != 4:
        print(simple_colors.red(CALL_SCRIPT_ERROR))
        return
    
    inputPath   = sys.argv[1]
    outputPath  = sys.argv[2]
    isZipped    = sys.argv[3].lower()
    
    if not os.path.exists(inputPath) or not(isZipped == "zip" or isZipped == "unzip"):
        print(simple_colors.red(CALL_SCRIPT_ERROR))
        return

    isZipped = True if isZipped == "unzip" else False
    
    if isZipped:      
        unzip(inputPath, outputPath)
    else:
        zip(inputPath, outputPath)
    
if __name__ == "__main__":
    main()
