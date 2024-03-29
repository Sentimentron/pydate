tmzabbrs = """ADT
ADT
AFT
AKDT
AKST
ALMT
AMST
AMST
AMT
AMT
ANAST
ANAT
AQTT
ART
AST
AST
AST
AST
AZOST
AZOT
AZST
AZT
BNT
BOT
BRST
BRT
BST
BST
BTT
CAST
CAT
CCT
CDT
CDT
CDT
CEST
CET
CET
CHADT
CHAST
CKT
CLST
CLT
COT
CST
CST
CST
CST
CST
CVT
CXT
ChST
DAVT
EASST
EAST
EAT
EAT
ECT
EDT
EDT
EDT
EDT
EEST
EEST
EEST
EET
EET
EET
EGST
EGT
EST
EST
EST
EST
ET
ET
ET
FJST
FJT
FKST
FKT
FNT
GALT
GAMT
GET
GFT
GILT
GMT
GMT
GST
GYT
HAA
HAA
HAC
HADT
HAE
HAE
HAP
HAR
HAST
HAT
HAY
HKT
HLV
HNA
HNA
HNA
HNC
HNC
HNE
HNE
HNE
HNP
HNR
HNT
HNY
HOVT
ICT
IDT
IOT
IRDT
IRKST
IRKT
IRST
IST
IST
IST
JST
KGT
KRAST
KRAT
KST
KUYT
LHDT
LHST
LINT
MAGST
MAGT
MART
MAWT
MDT
MESZ
MEZ
MHT
MMT
MSD
MSK
MST
MUT
MVT
MYT
NCT
NDT
NFT
NOVST
NOVT
NPT
NST
NUT
NZDT
NZDT
NZST
NZST
OMSST
OMST
PDT
PET
PETST
PETT
PGT
PHOT
PHT
PKT
PMDT
PMST
PONT
PST
PST
PT
PWT
PYST
PYT
RET
SAMT
SAST
SBT
SCT
SGT
SRT
SST
TAHT
TFT
TJT
TKT
TLT
TMT
TVT
ULAT
UYST
UYT
UZT
VET
VLAST
VLAT
VUT
WAST
WAT
WDT
WEST
WEST
WESZ
WET
WET
WEZ
WFT
WGST
WGT
WIB
WIT
WITA
WST
WST
WST
WT
YAKST
YAKT
YAPT
YEKST
YEKT""".split("\n")

def is_timezone(tz):
    return tz in tmzabbrs