# Tei-Parser 1.0

Authors: Michaela Falátková and Jan Marek

Tei-parser is a python application that transforms the content of TEI document that follows Lombard Press Schema 1.0.0 guidelines (https://lombardpress.org/schema/docs/diplomatic/) into a web presentation. 
The web presentation is a static display of pages of the TEI document. Each page contains an image and a transcribed content.

##  How to use
0. Install python (miniconda) - Download from https://docs.conda.io/en/latest/miniconda.html
1. Setup a specific python environment or use base one 
2. Clone the repository (or download it), cd to it
4. Install dependencies
5. Run the program from CLI
6. Copy the generated file(html) + images + bootstrap folders to a location 

## Detailed guide
Download and install miniconda (https://docs.conda.io/en/latest/miniconda.html)

Run Anaconda Prompt (miniconda3) -  search with windows
```
cd c:\tei-parser (or to a location where you downloaded this repository)
```
Python environment setup (Required for running the program)
```
pip install -r requirements.txt
```
Python environment setup (Required for running the program)

Run from CLI (from root folder)
```
python run.py --input_file_path ./_example/Paris-Lat-9765.xml --output_file_path output-full.html
```

## Example structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI>
  <teiHeader>
  </teiHeader>
  <text>
    <body>
      <div>  
        <pb facs="facsimiles/1r.jpg" n="1r"/>    
        <p>
          <note>NOTENOTENOTE</note>I De Adam et Eua.
        </p>
        <p>EXPLICIT LIBER I, A PRONCIPIO MVNDI VSQUE I</p>
      </div>
    </body>
  </text>
</TEI>
```

## Extracted fields

| Area  | Tag  | Desc  | Example  | Visualization  |
| --------- | --- |---------- | ------------- |------------- |
| teiHeader | title  | title  | | header, title  |
| | author  | author  | | header  |
| | editor  | editor  | | footer  |
| | editionStmt/edition/date  | data of translation  | |header  |
| | publicationStmt/authority/ref  | authority  | | footer  |
| | publicationStmt/availability  | license  | | footer  |
| | listWit/witness  | witness  | | header  |
| | encodingDesc/editorialDecl  | declaration  | | footer  |
| text  | pb  | page break  |``` <pb facs="" n="2v"/> ``` | will break page; facs - link to an image; n - above page
| | p  |paragraph  | ``` <p></p> ``` |same as html p  |
| | lb | line break  |``` </lb> ```  | not used
| | note  |note  | ``` <note></note> ```  |under text, types do not matter, number the notes, display the number in the text |
| | quote | quote  |``` <quote></quote> ```  | italica (nothing else)
| | ref  |reference  | ``` <ref><name>Horosii</name> narrat<title>historia</title><link>seznam.cz</link></ref>```  | link ``` <a href="seznam.cz"><u>Horosiii narrat historia</u></a> ```  |

