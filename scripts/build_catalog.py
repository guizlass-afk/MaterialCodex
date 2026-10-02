"""Curated factual reference data. Sources are linked per record/property. No runtime network."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
materials=[]
SOURCES={}
def source(id,title,url): SOURCES[id]={'title':title,'url':url,'accessed':'2026-10-02'};return id
def prop(v,condition='room',kind='typical',method='',source=None):
 d={'v':v,'condition':condition,'kind':kind}
 if method:d['method']=method
 if source:d['source']=source
 return d
def material(id,name,family,identity,condition,composition,src,properties,aliases=''):
 m={'id':id,'name':name,'family':family,'identity':identity,'condition':condition,'composition':composition,'source':src,'properties':properties,'aliases':aliases};materials.append(m);return m
core=source('core','Outokumpu · Core · Tables 1, 5, 7','https://www.outokumpu.com/en/products/product-ranges/-/media/files/products/core/outokumpu-core-range-datasheet.pdf')
# Selected cold-rolled C product rows, EN 10088-2, room temperature.
for id,en,uns,c,cr,ni,y,ts,elong in [
 ('304','1.4301','S30400',.04,18.1,8.1,230,[540,750],45),
 ('304L','1.4307','S30403',.02,18.1,8.1,220,[520,700],45),
 ('304LN','1.4311','S30453',.02,18.5,9.2,290,[550,750],40),
 ('305','1.4303','S30500',.04,17.7,12.5,220,[500,650],45),
 ('321','1.4541','S32100',.04,17.3,9.1,220,[520,720],40),
 ('347','1.4550','S34700',.05,17.5,9.5,220,[520,720],40),
 ('301LN','1.4318','S30153',.02,17.7,6.5,350,[650,850],35),
 ('301','1.4310','S30100',.1,17,7,250,[600,950],40)]:
  comp={'Fe':'balance','C':c,'Cr':cr,'Ni':ni}
  if id in ['304LN','301LN']:comp['N']=.14
  if id=='321':comp['Ti']='present'
  if id=='347':comp['Nb']='present'
  props={'density':prop(7900,'20 °C'),'young':prop(200,'20 °C'),'tensile':prop(ts,'20 °C','range','EN 10088-2 · C'),'yield':prop(y,'20 °C','minimum','Rp0.2 · EN 10088-2 · C'),'elongation':prop(elong,'20 °C','minimum','A80 · EN 10088-2 · C'),'thermal':prop(15,'20 °C'),'heat':prop(500,'20 °C'),'expansion':prop(16,'20–100 °C'),'resistivity':prop(.73e-6,'20 °C')}
  material('ss-'+id.lower(),'Core '+id+' / '+en,'metal','stainless','coldRolled',{'mode':'typicalMass','items':comp},core,props,'inox aço aço inoxidável stainless steel acero acier Edelstahl '+uns+' '+en+' '+id)
# Ferritic grade; no nickel concentration is inferred from a dash in the source.
material('ss-441','Core 441 / 1.4509','metal','stainless','coldRolled',{'mode':'typicalMass','items':{'Fe':'balance','C':.02,'Cr':17.6,'Ti':'present','Nb':'present'}},core,{'density':prop(7700,'20 °C'),'young':prop(220,'20 °C'),'tensile':prop([430,630],'20 °C','range','EN 10088-2 · C'),'yield':prop(250,'20 °C','minimum','Rp0.2 · EN 10088-2 · C'),'elongation':prop(18,'20 °C','minimum','A80 · EN 10088-2 · C'),'thermal':prop(25,'20 °C'),'heat':prop(460,'20 °C'),'expansion':prop(10,'20–100 °C'),'resistivity':prop(.6e-6,'20 °C')},'inox ferritic aço S43940')
al=source('hydro6061','Hydro · Alloy 6061 · 2019/01','https://www.hydro.com/globalassets/01-products--services/extruded-profiles/americas/ena-resources/alloy-data-sheets/hydro_2019_data_sheet_6061.pdf')
comp={'mode':'limitsMass','items':{'Al':'balance','Si':[.4,.8],'Fe':'≤ 0.7','Cu':[.15,.4],'Mn':'≤ 0.15','Mg':[.8,1.2],'Cr':[.04,.35],'Zn':'≤ 0.25','Ti':'≤ 0.15'}}
for temper,ts,y,elong,k,iacs,kind in [('T6',260,240,8,167,43,'minimum'),('T4',180,110,16,155,42,'minimum'),('O',150,110,16,180,47,'maximum')]:
 props={'density':prop(.098*.45359237/.0254**3,'room','converted','0.098 lb/in³'),'tensile':prop(ts,'wallLE630',kind),'yield':prop(y,'wallLE630',kind,'Rp0.2'),'elongation':prop(elong,'wallLE630','minimum','L0 = 2 in / 4D'),'thermal':prop(k,'25 °C'),'iacs':prop(iacs,'20 °C'),'expansion':prop(13.1*1.8,'20–100 °C','converted'),'melting':prop([(1080-32)/1.8,(1206-32)/1.8],'','range')}
 material('al6061-'+temper.lower(),'6061-'+temper,'metal','aluminium','extruded',comp,al,props,'alumínio aluminio aluminum aluminium AlMg1SiCu UNS A96061')
cu=source('c110','Copper Development Association · C11000','https://alloys.copper.org/alloy/C11000')
material('c11000','C11000 · ETP','metal','copper','physicalOnly',{'mode':'limitsMass','items':{'Cu + Ag':'≥ 99.90','O':'variable'}},cu,{'density':prop(.322*.45359237/.0254**3,'20 °C','converted','0.322 lb/in³'),'young':prop(17000*6.894757293168/1000,'room','converted'),'shear':prop(6400*6.894757293168/1000,'room','converted'),'thermal':prop(226*1.730734666,'20 °C','converted'),'heat':prop(.092*4186.8,'20 °C','converted'),'iacs':prop(101,'20 °C'),'expansion':prop(9.4*1.8,'20–100 °C','converted'),'melting':prop([(1949-32)/1.8,(1981-32)/1.8],'','range')},'cobre copper Cu Cu-ETP')
# Curbell engineering stock reference values. Specific gravity is not density.
psi=.006894757293168
for id,name,slug,condition,chem,sg,tensile,young,flex,elong,water,cte,service,hardness in [
 ('abs','ABS','abs','stock','acrylonitrileButadieneStyrene',1.04,4100,294000,9100,32,.30,5.6,160,'Rockwell R102'),
 ('pom-h','POM-H · Acetal','acetal','homopolymer','polyoxymethylene',1.42,10000,450000,14300,75,.25,6.8,185,'Rockwell M89 / R121; Shore D83'),
 ('pom-c','POM-C · Acetal','acetal','copolymer','polyoxymethylene',1.41,9800,430000,13000,75,.20,6.1,195,'Rockwell M80'),
 ('pa66','PA66 · Nylon 6/6','nylon','extruded','polyamide66',1.14,12400,470000,17000,90,1.2,4.5,210,'Rockwell M85 / R121; Shore D80'),
 ('pa6','PA6 · Nylon 6','nylon','cast','polyamide6',1.15,12000,400000,16000,20,.6,4.4,200,'Rockwell M85; Shore D85'),
 ('peek','PEEK','peek','stock','polyetheretherketone',1.32,16000,630000,25000,40,.1,2.6,480,'Rockwell M105 / R126; Shore D85'),
 ('ptfe','PTFE','ptfe','unfilled','polytetrafluoroethylene',2.15,[1500,3000],None,None,[100,200],None,8.9,500,'Shore D55'),
 ('hdpe','HDPE / PE-HD','hdpe','stock','polyethylene',.96,4000,None,None,600,.1,9,170,'Shore D69'),
 ('pc','PC · Polycarbonate','polycarbonate','unfilled','polycarbonate',1.2,9500,345000,13500,135,.15,3.8,240,'Rockwell M70 / R118; Shore D80'),
 ('pp-h','PP-H','polypropylene','homopolymer','polypropylene',.91,5400,None,None,None,None,None,180,'Shore D75'),
 ('pp-c','PP-C','polypropylene','copolymer','polypropylene',.90,3800,None,None,None,None,None,None,'Shore D75')]:
 src='plastic-'+slug
 source(src,'Curbell Plastics · '+slug,'https://www.curbellplastics.com/materials/plastics/'+slug+'/')
 props={'specificGravity':prop(sg,'sourceConditions','typical','ASTM D792'),'tensile':prop([v*psi for v in tensile] if isinstance(tensile,list) else tensile*psi,'sourceConditions','range' if isinstance(tensile,list) else 'typical','ASTM D638'),'hardness':prop(hardness,'sourceConditions')}
 if young:props['young']=prop(young*psi/1000,'sourceConditions','typical','ASTM D638')
 if flex:props['flexural']=prop(flex*psi,'sourceConditions','typical','ASTM D790')
 if elong:props['elongation']=prop(elong,'sourceConditions','range' if isinstance(elong,list) else 'typical','ASTM D638')
 if water is not None:props['waterAbsorption']=prop(water,'24 h','typical','ASTM D570')
 if cte:props['expansion']=prop(cte*18,'sourceConditions','converted','ASTM D696')
 if service:props['service']=prop((service-32)/1.8,'air','typical')
 material(id,name,'polymer',chem,condition,{'mode':'polymerBase','items':{}},src,props,'plastic plástico plastico polymer '+chem)
# Technical ceramics: grade-specific producer values; flexure is not tensile strength.
cer=source('alumina','CoorsTek · Alumina','https://www.coorstek.com/en/materials/alumina/')
for id,purity,rho,flex,e,comp,k,cp,eps in [('AD-94',94,3.70,308,303,2103,22.4,880,9.1),('AD-96',96,3.72,343,303,2068,24.7,880,9),('AD-995',99.5,3.9,300,370,2600,30,880,9.7),('AD-998',99.8,3.92,320,380,2650,31,880,9.8)]:
 material(id.lower(),'Al₂O₃ · '+id,'ceramic','alumina','sintered',{'mode':'nominalMass','items':{'Al₂O₃':purity}},cer,{'density':prop(rho*1000,'sourceConditions'),'flexural':prop(flex,'20 °C','typical','4-point MOR'),'young':prop(e,'20 °C'),'compressive':prop(comp,'20 °C'),'thermal':prop(k,'20 °C'),'heat':prop(cp,'100 °C'),'expansion':prop(8.2,'25–1000 °C'),'permittivity':prop(eps,'25 °C · 1 MHz'),'resistivity':prop(1e12,'25 °C','greater'),'toughness':prop([4,5],'sourceConditions','range')},'alumina óxido de alumínio aluminum oxide')
zr=source('zirconia','CoorsTek · Zirconia','https://www2.coorstek.com/en/materials/zirconia/')
for id,label,rho,flex,e,comp,kic,cte in [('dura-z','Dura-Z · MgO-PSZ',5720,620,200,1750,11,10.2),('ytzp','Y-TZP · sintered',6020,1240,210,2500,13,10.3),('technox2000','Technox 2000',6020,1000,210,2000,10,10.3),('ytzp-hip','Y-TZP · HIP',6070,1720,210,2500,13,10.3)]:
 material(id,'ZrO₂ · '+label,'ceramic','zirconia','gradeSpecific',{'mode':'base','items':{'ZrO₂':'base','MgO' if id=='dura-z' else 'Y₂O₃':'present'}},zr,{'density':prop(rho,'sourceConditions'),'flexural':prop(flex,'20 °C','typical','4-point MOR'),'young':prop(e,'20 °C'),'compressive':prop(comp,'20 °C'),'thermal':prop(2.2,'20 °C'),'toughness':prop(kic,'sourceConditions'),'expansion':prop(cte,'25–1000 °C'),'resistivity':prop(1e11,'25 °C','greater')},'zirconia zircônia zirconium oxide')
sic=source('sic','CoorsTek · Silicon carbide','https://www2.coorstek.com/en/materials/silicon-carbide/')
for id,flex,k,kic,cte,service in [('CeraSiC-B',450,170,3.5,4.5,1500),('SC-RB',462,125,4,4.3,1000),('UltraSiC-LP',620,80,6,4.8,1000)]:
 material(id.lower(),'SiC · '+id,'ceramic','siliconCarbide','gradeSpecific',{'mode':'base','items':{'SiC':'base'}},sic,{'flexural':prop(flex,'20 °C','typical','MOR'),'thermal':prop(k,'20 °C'),'toughness':prop(kic,'sourceConditions'),'expansion':prop(cte,'sourceConditions'),'service':prop(service,'sourceConditions')},'carbeto carboneto de silício silicon carbide')
sn=source('silicon-nitride','CoorsTek · Silicon nitride','https://www2.coorstek.com/en/materials/silicon-nitride/')
for id,flex,k,kic,cte,service in [('NBD-200',900,29,5.5,2.9,1400),('SN-101C',1000,34,6.5,3.7,1400),('SN-102',1000,18,6,3.5,1000)]:
 material(id.lower(),'Si₃N₄ · '+id,'ceramic','siliconNitride','gradeSpecific',{'mode':'base','items':{'Si₃N₄':'base'}},sn,{'flexural':prop(flex,'20 °C','typical','MOR'),'thermal':prop(k,'20 °C'),'toughness':prop(kic,'sourceConditions'),'expansion':prop(cte,'sourceConditions'),'service':prop(service,'sourceConditions'),'resistivity':prop(1e12,'25 °C','greater')},'nitreto de silício silicon nitride')
# Gas values at 25 C and 1.013 bar; source tab explicitly selected.
for id,formula,cas,molar,rho,cp,cv,k,visc,z,gamma,boil,liquid in [
 ('nitrogen','N₂','7727-37-9',28.013,1.145,1041.4,743.16,.025835,1.7805e-5,.9998,1.4013,-195.8,806.11),
 ('oxygen','O₂','7782-44-7',31.999,1.3085,919.62,658.46,.02634,2.055e-5,.99935,1.3967,-182.96,1141.2),
 ('argon','Ar','7440-37-1',39.948,1.6335,521.55,312.38,.017746,2.2624e-5,.99937,1.6696,-185.85,1395.4),
 ('helium','He','7440-59-7',4.003,.1635,5192.9,3116,.15531,1.9846e-5,1.0005,1.6665,-268.93,124.74),
 ('hydrogen','H₂','1333-74-0',2.016,.0823,14306.3,10179.6,.18488,8.9154e-6,1.0006,1.4054,-252.78,70.516),
 ('methane','CH₄','74-82-8',16.043,.6567,2231.6,1708.5,.033931,1.1067e-5,.99825,1.3062,-161.48,422.36),
 ('carbon-dioxide','CO₂','124-38-9',44.010,1.8075,850.85,657.49,.016643,1.4932e-5,.99496,1.2941,None,None)]:
 src=source('gas-'+id,'Air Liquide · '+id,'https://encyclopedia.airliquide.com/'+id)
 props={key:prop(v,'25 °C · 1.013 bar') for key,v in {'density':rho,'heat':cp,'cv':cv,'thermal':k,'viscosity':visc,'z':z,'gamma':gamma}.items()};props['molarMass']=prop(molar,'');
 if boil is not None:props['boiling']=prop(boil,'1.013 bar')
 material(id,formula,'gas',id,'gas25',{'mode':'formula','items':{formula:'base'}},src,props,cas+' '+id)
 if liquid is not None:
  material(id+'-liquid',formula+' (L)','liquid',id,'cryogenic',{'mode':'formula','items':{formula:'base'}},src,{'density':prop(liquid,str(boil)+' °C · 1.013 bar'),'boiling':prop(boil,'1.013 bar'),'molarMass':prop(molar,'')},cas+' '+id+' liquid liquido líquido')

# Additional engineering grades, tied to the exact product/condition in each source.
supra=source('supra','Outokumpu · Supra · Tables 1, 5, 7','https://www.outokumpu.com/-/media/files/products/supra/outokumpu-supra-range-datasheet.pdf')
for grade,en,c,cr,ni,ts,cte in [('316','1.4401',.04,17.2,10.1,[530,680],16),('316L','1.4404',.02,17.2,10.1,[530,680],16),('316Ti','1.4571',.04,16.8,10.9,[540,690],16.5)]:
 comp={'Fe':'balance','C':c,'Cr':cr,'Ni':ni,'Mo':2.1}
 if grade=='316Ti':comp['Ti']='present'
 material('ss-'+grade.lower(),'Supra '+grade+' / '+en,'metal','stainless','coldRolled',{'mode':'typicalMass','items':comp},supra,{'density':prop(8000,'20 °C'),'young':prop(200,'20 °C'),'tensile':prop(ts,'20 °C','range','EN 10088-2 · C'),'yield':prop(240,'20 °C','minimum','Rp0.2 · EN 10088-2 · C'),'elongation':prop(40,'20 °C','minimum','A80 · EN 10088-2 · C'),'thermal':prop(15,'20 °C'),'heat':prop(500,'20 °C'),'resistivity':prop(.75e-6,'20 °C'),'expansion':prop(cte,'20–100 °C')},'inox stainless aço '+grade+' '+en)
for id,name,chem,condition,y,ts,elong,hard in [
 ('c45','C45 · SB1672 · +U',{'Fe':'balance','C':[.42,.50],'Si':[.1,.4],'Mn':[.5,.9],'P':'≤ 0.045','S':[.020,.045],'Cr':'≤ 0.40','Ni':'≤ 0.40','Mo':'≤ 0.10'},'C45 · +U · d < 16 mm',320,[590,740],14,'165–220 HB'),
 ('42crmo4','42CrMo4 · M (6082) · +QT',{'Fe':'balance','C':[.38,.45],'Si':[.15,.40],'Mn':[.6,.9],'P':'≤ 0.025','S':[.020,.035],'Cr':[.90,1.20],'Mo':[.15,.30]},'42CrMo4 · +QT · 25 < d < 40 mm',750,[1000,1200],11,'300–350 HB')]:
 src=source(id,'Ovako Steel Navigator · '+id,'https://steelnavigator.ovako.com/steel-grades/'+id+'/')
 material(id,name,'metal','steel',condition,{'mode':'limitsMass','items':chem},src,{'density':prop(7800,'room'),'young':prop(210,'room'),'shear':prop(80,'room'),'poisson':prop(.3,'room'),'tensile':prop(ts,condition,'range'),'yield':prop(y,condition,'minimum','ReL'),'elongation':prop(elong,condition,'minimum','A5'),'hardness':prop(hard,condition,'range'),'thermal':prop([40,45],'room','range'),'heat':prop([460,480],'50 / 100 °C','range'),'expansion':prop(12,'20–300 °C'),'resistivity':prop([.20e-6,.25e-6],'room','range')},'steel aço acero acier Stahl')
ti=source('timet','TIMET · TIMETAL 6-4 · historical datasheet 2000','https://www.timet.com/documents/datasheets/alpha-and-beta-alloys/timetal-6-4.pdf')
material('ti6al4v','Ti-6Al-4V · Grade 5','metal','titanium','annealedTi',{'mode':'limitsMass','items':{'Ti':'balance','Al':[5.5,6.75],'V':[3.5,4.5],'N':'≤ 0.05','C':'≤ 0.08','O':'≤ 0.20','Fe':'≤ 0.40','H':'≤ 0.015'}},ti,{'density':prop(4420,'22 °C'),'thermal':prop(6.6,'20 °C'),'heat':prop(580,'20 °C'),'resistivity':prop(1.68e-6,'0 °C'),'expansion':prop(9,'0–100 °C'),'young':prop([107,122],'20 °C','range'),'shear':prop([41,45],'20 °C','range'),'poisson':prop(.31,'room'),'tensile':prop(895,'20 °C','minimum','ASTM B348 · longitudinal · d < 3 in'),'yield':prop(828,'20 °C','minimum','Rp0.2 · ASTM B348 · longitudinal · d < 3 in'),'elongation':prop(10,'20 °C','minimum','ASTM B348 · longitudinal · d < 3 in')},'titanio titânio titanium UNS R56400')
for id,name,identity,sg,ts,e,flex,water,cte,service,hard in [('acrylic','PMMA · Acrylic','pmma',1.19,10000,400000,17000,.20,72,160,'Rockwell M95'),('pvc','PVC · Rigid','pvc',1.42,7500,411000,12800,.06,57.6,140,'Rockwell R115 / Shore D89')]:
 src=source('plastic-'+id,'Curbell Plastics · '+id,'https://www.curbellplastics.com/materials/plastics/'+id+'/')
 material(id,name,'polymer',identity,'stock',{'mode':'polymerBase','items':{}},src,{'specificGravity':prop(sg,'sourceConditions','typical','ASTM D792'),'tensile':prop(ts*psi,'sourceConditions','typical','ASTM D638'),'young':prop(e*psi/1000,'sourceConditions','typical','ASTM D638'),'flexural':prop(flex*psi,'sourceConditions','typical','ASTM D790'),'waterAbsorption':prop(water,'24 h','typical','ASTM D570'),'expansion':prop(cte,'sourceConditions','converted','ASTM D696'),'service':prop((service-32)/1.8,'air'),'hardness':prop(hard,'sourceConditions')},'acrílico acrylic metacrilato' if id=='acrylic' else 'policloreto vinila polyvinyl chloride')
src=source('g10','Curbell Plastics · G10 / FR-4 Glass Epoxy','https://www.curbellplastics.com/materials/plastics/g10-fr-4-glass-epoxy/')
material('g10-fr4','G10 / FR-4','composite','glassEpoxy','sourceConditions',{'mode':'base','items':{}},src,{'specificGravity':prop(1.8,'sourceConditions'),'tensile':prop(38000*psi,'sourceConditions','typical','ASTM D638'),'flexural':prop(60000*psi,'sourceConditions','typical','ASTM D790'),'flexuralModulus':prop(2400000*psi/1000,'sourceConditions','typical','ASTM D790'),'compressive':prop(55000*psi,'10%','typical','ASTM D695'),'hardness':prop('Rockwell M115','sourceConditions'),'service':prop(140,'air')},'glass epoxy fibra vidro epóxi laminado composite')
for m in materials:
 if m['id']=='ad-998':m['composition']['items']['Al₂O₃']='≥ 99.8'

def build():
 ids=[m['id'] for m in materials];assert len(ids)==len(set(ids))
 for m in materials:
  for key,p in m['properties'].items():assert p.get('source',m['source']) in SOURCES
 data={'version':'2026-10-02','sources':SOURCES,'materials':materials}
 (ROOT/'materials.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'materials.js').write_text('const MaterialData = '+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
 print(len(materials),'materials;',sum(len(m['properties']) for m in materials),'source-backed properties')
if __name__=='__main__':build()
