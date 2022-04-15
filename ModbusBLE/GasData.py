class GasBean:
    name: str=''
    formula: str=''
    number: bytes=''

    def __init__(self,name: str,formula: str,number: bytes):
        self.name = name
        self.formula = formula
        self.number = number

class UnitBean:
    name: str =''
    number: bytes=''

    def __init__(self,name: str, number: bytes):
        self.name = name
        self.number = number



class Gas:
    gasList=[
        GasBean("사용하지않음", "사용하지않음", bytes.fromhex("00")),
        GasBean("가연성", "EX", bytes.fromhex("01")),
        GasBean("이산화탄소", "CO2", bytes.fromhex("02")),
        GasBean("일산화탄소", "CO", bytes.fromhex("03")),
        GasBean("산소", "O2", bytes.fromhex("04")),
        GasBean("황화수소", "H2S", bytes.fromhex("05")),
        GasBean("암모니아", "NH3", bytes.fromhex("06")),
        GasBean("수소", "H2", bytes.fromhex("07")),
        GasBean("사용하지않음", "CH2O", bytes.fromhex("08")), #
        GasBean("오존", "O3", bytes.fromhex("09")),
        GasBean("염소", "Cl2", bytes.fromhex("10")),
        GasBean("질소", "N2", bytes.fromhex("11")),
        GasBean("이산화황", "SO2", bytes.fromhex("12")),
        GasBean("사용하지않음", "CH4", bytes.fromhex("13")),
        GasBean("총휘발성유기 화합물", "TVOC", bytes.fromhex("14")),
        GasBean("휘발성유기 화합물", "VOC", bytes.fromhex("15")),
        GasBean("사용하지않음", "VOCs", bytes.fromhex("16")),
        GasBean("사용하지않음", "PID", bytes.fromhex("17")),
        GasBean("일산화질소", "NO", bytes.fromhex("18")),
        GasBean("이산화질소", "NO2", bytes.fromhex("19")),
        GasBean("사용하지않음", "NOx", bytes.fromhex("20")),
        GasBean("산화에틸렌/에틸렌옥사이드", "ETO", bytes.fromhex("21")),
        GasBean("인화수소 / 포스핀", "PH3", bytes.fromhex("22")),
        GasBean("이산화염소", "ClO2", bytes.fromhex("23")),
        GasBean("염화수소", "HCl", bytes.fromhex("24")),
        GasBean("사용하지않음", "HBr", bytes.fromhex("25")),
        GasBean("시안화수소", "HCN", bytes.fromhex("26")),
        GasBean("사용하지않음", "COCl2", bytes.fromhex("27")),
        GasBean("메틸브로마이드", "CH3Br", bytes.fromhex("28")),
        GasBean("플루오린화수푸릴", "SO2F2", bytes.fromhex("29")),
        GasBean("벤젠", "C6H6", bytes.fromhex("30")),
        GasBean("톨루엔", "C7H8", bytes.fromhex("31")),
        GasBean("에틸벤젠", "C8H10", bytes.fromhex("32")),
        GasBean("프로판", "C3H8", bytes.fromhex("33")),
        GasBean("실란", "SIH4", bytes.fromhex("34")),
        GasBean("불소", "F2", bytes.fromhex("35")),
        GasBean("불화수소", "HF", bytes.fromhex("36")),
        GasBean("사용하지않음", "He", bytes.fromhex("37")),
        GasBean("사용하지않음", "Ar", bytes.fromhex("38")),
        GasBean("사용하지않음", "B2H6", bytes.fromhex("39")),
        GasBean("사용하지않음", "GeH4", bytes.fromhex("40")),
        GasBean("사용하지않음", "C4H8S", bytes.fromhex("41")),
        GasBean("하이드라이진", "N2H4", bytes.fromhex("42")),
        GasBean("에탄올 / 에틸렌", "C2H4", bytes.fromhex("43")),
        GasBean("사용하지않음", "CH3CH3", bytes.fromhex("44")),
        GasBean("사용하지않음", "AsH3", bytes.fromhex("45")),
        GasBean("사용하지않음", "Br2", bytes.fromhex("46")),
        GasBean("사용하지않음", "C2H2", bytes.fromhex("47")),
        GasBean("사용하지않음", "N2O", bytes.fromhex("48")),
        GasBean("육불화황", "SF6", bytes.fromhex("49")),
        GasBean("사용하지않음", "BCl3", bytes.fromhex("50")),
        GasBean("사용하지않음", "CS2", bytes.fromhex("51")),
        GasBean("사용하지않음", "C2H4O", bytes.fromhex("52")),
        GasBean("사용하지않음", "C3H3N", bytes.fromhex("53")),
        GasBean("사용하지않음", "C4H6", bytes.fromhex("54")),
        GasBean("사용하지않음", "CH4O", bytes.fromhex("55")),
        GasBean("사용하지않음", "CH3NH2", bytes.fromhex("56")),
        GasBean("사용하지않음", "CH3SH", bytes.fromhex("57")),
        GasBean("사용하지않음", "C2H6S", bytes.fromhex("58")),
        GasBean("사용하지않음", "C2H6S2", bytes.fromhex("59")),
        GasBean("사용하지않음", "C2H3Cl", bytes.fromhex("60")),
        GasBean("사용하지않음", "C3H8O", bytes.fromhex("61")),
        GasBean("사용하지않음", "C2H6O", bytes.fromhex("62")),
        GasBean("사용하지않음", "CH3COCH3", bytes.fromhex("63")),
        GasBean("사용하지않음", "C4H8O", bytes.fromhex("64")),
        GasBean("사용하지않음", "CH3Cl", bytes.fromhex("65")),
        GasBean("사용하지않음", "C6H5CH2Cl", bytes.fromhex("66")),
        GasBean("사용하지않음", "C2H7N", bytes.fromhex("67")),
        GasBean("사용하지않음", "C8H8", bytes.fromhex("68")),
        GasBean("사용하지않음", "C4H10", bytes.fromhex("69")),
        GasBean("탄화수소 / 하이드로카본", "HC", bytes.fromhex("70")),
        GasBean("사용하지않음", "C4H8O2", bytes.fromhex("71")),
        GasBean("사용하지않음", "C3H4O2", bytes.fromhex("72")),
        GasBean("사용하지않음", "C2H4O2", bytes.fromhex("73")),
        GasBean("과산화수소", "H2O2", bytes.fromhex("74")),
        GasBean("사용하지않음", "C2H4O", bytes.fromhex("75")),
        GasBean("사용하지않음", "C7H6O2", bytes.fromhex("76")),
        GasBean("사용하지않음", "C3H7NO", bytes.fromhex("77")),
        GasBean("사용하지않음", "C4H9NO", bytes.fromhex("78")),
        GasBean("사용하지않음", "H2Se", bytes.fromhex("79")),
        GasBean("사용하지않음", "CCl3NO2", bytes.fromhex("80")),
        GasBean("사용하지않음", "CHBr2Cl", bytes.fromhex("81")),
        GasBean("사용하지않음", "C6H14", bytes.fromhex("82")),
        GasBean("사용하지않음", "C5H12", bytes.fromhex("83")),
        GasBean("사용하지않음", "C2H6O", bytes.fromhex("84")),
        GasBean("사용하지않음", "C2H3NO", bytes.fromhex("85")),
        GasBean("사용하지않음", "C4H6O3", bytes.fromhex("86")),
        ]
        
    unitList=[
        UnitBean(r"ppm",bytes.fromhex("00")),
        UnitBean(r"mg/m3",bytes.fromhex("01")),
        UnitBean(r"ppb",bytes.fromhex("02")),
        UnitBean(r"ug/m3",bytes.fromhex("03")),
        UnitBean(r"%Vol",bytes.fromhex("04")),
        UnitBean(r"g/m3",bytes.fromhex("05")),
        UnitBean(r"%LEL",bytes.fromhex("06")),
        UnitBean(" ",bytes.fromhex("07")),
        UnitBean(r"umol/mol",bytes.fromhex("08")),
        UnitBean(r"nmol/mol",bytes.fromhex("09")),
        ]

    def getGas(self,number:int) -> GasBean:
        return self.gasList[number]

    def getUnit(self,number:int)-> UnitBean:
        return self.unitList[number]


