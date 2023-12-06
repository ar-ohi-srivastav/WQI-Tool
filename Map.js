import React, { useEffect } from 'react'
import GoogleMapReact from 'google-map-react'
import axios from 'axios';
import { MapContainer, TileLayer, Marker, River, Popup,Circle,CircleMarker,Polyline} from 'react-leaflet'
import './Map.css'
import { StyleSheet } from 'react-native';
import L from 'leaflet';
import LeafletMap from "./LeafletMap";
import Button from '@mui/material/Button';
import { createTheme, ThemeProvider  } from '@mui/material/styles';
require('leaflet');
require('leaflet-river');


const theme = createTheme({
  status: {
    danger: '#e53e3e',
  },
  palette: {
    primary: {
      main: '#0971f1',
      darker: '#053e85',
    },
    neutral: {
      main: '#0876F1',
      contrastText: '#ffffff',
    },
  },
});

const AnyReactComponent = ({ text }) => <div>{text}</div>;

const center = [13.237427429986727, 75.17831168101472]
const limeOptions = { color: 'lime', weight : 10 }


const markers =[[ 13.237427429986727,  75.17831168101472], 
  [ 13.237027048053541,  75.178080838913], 
  [ 13.236956127573029,  75.17802598249897], 
  [ 13.236029411797205,  75.1768999615639], 
  [ 13.235922613451873,  75.17673710658472], 
  [ 13.23577993745902,  75.17650996672812], 
  [ 13.235650208083532,  75.17623759916569], 
  [ 13.235572612293685,  75.17610731517196], 
  [ 13.235458304469674,  75.17597703118251], 
  [ 13.23527891617671,  75.17586903261738], 
  [ 13.235044459643468,  75.17578760512241], 
  [ 13.234791646832667,  75.17576703396429], 
  [ 13.234515471487304,  75.17576789109576], 
  [ 13.23432607008217,  75.17580560488248], 
  [ 13.234119981161278,  75.17587588966605],
  [ 13.234040650475047,  75.17587879338807]]
const markers1 = [[ 13.234040650475047,  75.17587879338807], 
  [ 13.233868836129588,  75.17591788910991], 
  [ 13.233616856469359,  75.17593160321377], 
  [ 13.233432460590144,  75.17589817508477], 
  [ 13.233230542774509,  75.17585103285138], 
  [ 13.23296854998534,  75.17577474814769], 
  [ 13.232644813285235,  75.17570789189129], 
  [ 13.232533007206891,  75.17569246352424], 
  [ 13.232285198043147,  75.17567103523751], 
  [ 13.232230129300875,  75.17567103523749], 
  [ 13.232058248007645,  75.17563674997876], 
  [ 13.231942269783932,  75.17557332224459], 
  [ 13.23185549467621,  75.17547732352003], 
  [ 13.231681109987598,  75.17524418374725], 
  [ 13.231529513097303,  75.17503046464478], 
  [ 13.230459839032067,  75.17384076611546], 
  [ 13.23031215355245,  75.17370791073228], 
  [ 13.230054329537667,  75.17350991335209], 
  [ 13.229926669004453,  75.17339762912961], 
  [ 13.229659666360547,  75.17328277350416], 
  [ 13.229357619267068,  75.17318334624832], 
  [ 13.22912566019424,  75.17315334664502], 
  [ 13.229000502332488,  75.17315248951355], 
  [ 13.228960451797068,  75.17315591804135], 
  [ 13.228568290014774,  75.17330334465993], 
  [ 13.228241209912113,  75.17339934338607], 
  [ 13.2281544334789,  75.17343362864611], 
  [ 13.227886594509274,  75.17350391342642], 
  [ 13.22774558259194,  75.17358534092095], 
  [ 13.227637111834625,  75.17367791111963], 
  [ 13.227479411951089,  75.17391362227947], 
  [ 13.227228260074247,  75.17448447187077], 
  [ 13.227061381608484,  75.17480761044433],
  [ 13.226919318280471,  75.17499314466153]]
const markers2 = [[ 13.226919318280471,  75.17499314466153], 
  [ 13.226887827886447,  75.17503817880959], 
  [ 13.226804388546496,  75.17508874957409], 
  [ 13.226668382371814,  75.1750973208888], 
  [ 13.226540720065163,  75.17505703570973], 
  [ 13.226297076778684,  75.17479218208257], 
  [ 13.22606094281373,  75.17457447068223], 
  [ 13.225828146208428,  75.1744999002417], 
  [ 13.22561787811531,  75.1744476152209], 
  [ 13.225325004397416,  75.17442618693313], 
  [ 13.225068009511494,  75.17443132972194], 
  [ 13.224903881177765,  75.17442905451075], 
  [ 13.224692777886446,  75.17437334096374], 
  [ 13.224538777150734,  75.17424332300553], 
  [ 13.224409444925588,  75.17399218348503], 
  [ 13.224314323108938,  75.17391675590771], 
  [ 13.22422337327403,  75.17387989925453], 
  [ 13.224050651934553,  75.17387047080837], 
  [ 13.223983065285545,  75.17387561360161], 
  [ 13.223766954778315,  75.1739484697765], 
  [ 13.223448212285614,  75.17403589719122], 
  [ 13.223175361705733,  75.17407018244998], 
  [ 13.222898338783157,  75.17412589599361], 
  [ 13.222441083393967,  75.17422789464254], 
  [ 13.22214486822032,  75.17438903537087], 
  [ 13.221835302124282,  75.17456646158776], 
  [ 13.221346350571777,  75.1750264903009], 
  [ 13.221079338532627,  75.17523563038154], 
  [ 13.220612901171222,  75.17571219549662], 
  [ 13.22041931689213,  75.17593076402129], 
  [ 13.220179005153923,  75.17624104562958], 
  [ 13.220127271344353,  75.17635847265163], 
  [ 13.220111417433628,  75.17652732755109], 
  [ 13.220103907686088,  75.17667903982115], 
  [ 13.220198132631534,  75.17685420122847], 
  [ 13.220343320986922,  75.17707191262167],
  [ 13.220373186780114,  75.1772472340153]]
const markers3 =  [[ 13.220373186780114,  75.1772472340153], 
  [ 13.220429265780096,  75.1773453375728],
  [ 13.220475158616907,  75.1776299052206],
  [ 13.220479330693939,  75.1778081885863],
  [ 13.220451794993364,  75.17812189870406],
  [ 13.220354168392362,  75.17831046764296],
  [ 13.220253204089897,  75.17843646596894],
  [ 13.220175603393763,  75.17851960773045],
  [ 13.219945304424582,  75.17859503529975],
  [ 13.219746713106318,  75.1786258920387],
  [ 13.219266196905993,  75.17858217833351],
  [ 13.219083459010863,  75.17856298231379],
  [ 13.218864006475359,  75.17851069729323],
  [ 13.218589481923152,  75.17849441179672],
  [ 13.21799286974403,  75.17861698161224],
  [ 13.21742726733764,  75.17881513009978],
  [ 13.216737268471704,  75.17905183504173],
  [ 13.216530986500342,  75.17916649948216],
  [ 13.216384761200707,  75.1794072277377],
  [ 13.216107977356089,  75.18027760455934],
  [ 13.215995044235276,  75.1805518604312],
  [ 13.215789965713759,  75.18116679040796],
  [ 13.215555612803715,  75.1815925910885],
  [ 13.215289304984893,  75.18197068542959],
  [ 13.21518812179289,  75.18204645783375],
  [ 13.215041895688525,  75.18212223023775],
  [ 13.214885224767835,  75.18216916889355],
  [ 13.214778265292601,  75.18215720902],
  [ 13.214655483972756,  75.18208227818147],
  [ 13.214565088368953,  75.18193615624256]]
const markers4 = [[ 13.214565088368953,  75.18193615624256], 
  [ 13.214532105433275,  75.18187440698517],
  [ 13.214173067001747,  75.18147811060358],
  [ 13.213870821510051,  75.18121391300984],
  [ 13.21359165647452,  75.18099312704277],
  [ 13.213522243363654,  75.18093767085774],
  [ 13.213354494930883,  75.18089013698486],
  [ 13.21328893803237,  75.18089409814513],
  [ 13.2131867463744,  75.18095153490819],
  [ 13.213032494734158,  75.18116741791417],
  [ 13.213024782149581,  75.18156749467755],
  [ 13.213109620566467,  75.18191409583395],
  [ 13.21311154871197,  75.18205669745258],
  [ 13.213047919902575,  75.18213988173011],
  [ 13.212833895593828,  75.18227059990458],
  [ 13.212696997065477,  75.18236962881241],
  [ 13.211430200020935,  75.18295587993802],
  [ 13.211119766261259,  75.18308065635432],
  [ 13.21107734671064,  75.18314799600756],
  [ 13.211038783476404,  75.18340150999624],
  [ 13.211113981773584,  75.18367681039224],
  [ 13.21127787542651,  75.18408679004581],
  [ 13.211347289175727,  75.18419770241584],
  [ 13.211339576537908,  75.18438387675128],
  [ 13.211274019106513,  75.18457005108671],
  [ 13.21089995577879,  75.18473641964178],
  [ 13.210325362530682,  75.1848413902898],
  [ 13.209976363947769,  75.18495428326257],
  [ 13.209692922750484,  75.18510282662407],
  [ 13.209318856999687,  75.18536822408096],
  [ 13.209190537893152,  75.18547529923937]]
const markers5 = [[ 13.209190537893152,  75.18547529923937], 
  [ 13.208871519876618,  75.18572076700474],
  [ 13.208651707363352,  75.18656251268479],
  [ 13.208509021948359,  75.18681206551739],
  [ 13.208337413696741,  75.18704379317555],
  [ 13.20812338526741,  75.18725967618154],
  [ 13.207616272107515,  75.18783404383714],
  [ 13.207159290898117,  75.18804398513133],
  [ 13.206436217612174,  75.18815093635001],
  [ 13.205691931951886,  75.18836087763546],
  [ 13.204815189860703,  75.1886133719467],
  [ 13.204192095630924,  75.1889485358679],
  [ 13.203420808017263,  75.18970115555406],
  [ 13.202488219926257,  75.19082317213109]]
const markers6 = [[ 13.202488219926257,  75.19082317213109], 
  [ 13.202038268884664,  75.19180651007395],
  [ 13.201394238224255,  75.19231749922109],
  [ 13.201043298641128,  75.19247594546906],
  [ 13.20074827761325,  75.19254328512349],
  [ 13.200474466935587,  75.19254724627957],
  [ 13.200005902873269,  75.19234918847316],
  [ 13.199845858143478,  75.19231353806752],
  [ 13.199606754995262,  75.192339285582],
  [ 13.199473705561449,  75.19242445043757],
  [ 13.199417786212562,  75.1927076730968],
  [ 13.199705095825466,  75.19380095222232],
  [ 13.200158234486338,  75.1943654170007],
  [ 13.20026043159761,  75.19457337769454],
  [ 13.200254646856612,  75.19471795989121],
  [ 13.200179445211068,  75.19481302763697],
  [ 13.200032898348107,  75.19484075572947],
  [ 13.199784154129482,  75.19483283341732],
  [ 13.19938500590048,  75.19478331896642],
  [ 13.19854621399386,  75.19495562929083],
  [ 13.198093072349156,  75.19519131809437],
  [ 13.19796195034822,  75.19543096804946],
  [ 13.197979882164974,  75.19550484036917]]
const markers7 = [[ 13.197979882164974,  75.19550484036917], 
  [ 13.198029439618136,  75.19563100643114],
  [ 13.198148991993364,  75.19573597706709],
  [ 13.198509577028865,  75.19589640388806],
  [ 13.198634913948645,  75.19604098608472],
  [ 13.198895228898389,  75.19682727560999],
  [ 13.19919989344606,  75.19712436233898],
  [ 13.199469849045949,  75.19723131355296],
  [ 13.20023729263663,  75.19723725528898],
  [ 13.200480251665722,  75.19717981852044],
  [ 13.200730923418803,  75.19708475077468],
  [ 13.201207199052618,  75.19715803214972],
  [ 13.201669976095491,  75.19711247885488],
  [ 13.202522254872877,  75.19685896486685],
  [ 13.203023593941145,  75.1966074314473],
  [ 13.203256909088791,  75.19661535375745],
  [ 13.203717754028228,  75.19680152809289],
  [ 13.20406868977002,  75.19716199330995],
  [ 13.204492897133354,  75.19783538988074],
  [ 13.204546887107174,  75.1980176030601],
  [ 13.204539174254501,  75.19824338895627],
  [ 13.204199660056243,  75.1987411281844]]
const markers8 = [[ 13.204199660056243,  75.1987411281844], 
  [ 13.20417088525286,  75.19879398967251],
  [ 13.204043622955398,  75.19925348380568],
  [ 13.204194945813592,  75.20006906366713],
  [ 13.204347274823494,  75.20028494667311],
  [ 13.204586373330972,  75.20047508216462],
  [ 13.204783050968693,  75.20074246022035],
  [ 13.204815830561143,  75.20113857584933],
  [ 13.204815830563357,  75.20195853517934],
  [ 13.204923810357261,  75.20229127230891],
  [ 13.20529788285217,  75.20290921268193],
  [ 13.205744585032342,  75.20346574574381],
  [ 13.206641198119275,  75.2038361138527],
  [ 13.206814735751534,  75.20400248240776],
  [ 13.206834017707795,  75.20451743272058],
  [ 13.206895719942448,  75.20468380127564],
  [ 13.206999842431467,  75.20506803344291],
  [ 13.206953565775189,  75.20545226560039],
  [ 13.206577567629836,  75.2061038757744],
  [ 13.206504296124054,  75.20634946748564],
  [ 13.20656548986791,  75.20651798069647]]
const markers9 = [[ 13.20656548986791,  75.20651798069647], 
  [ 13.206587208610237,  75.20656138933555],
  [ 13.207582495175812,  75.20791715681396],
  [ 13.20863335602252,  75.20886981487617],
  [ 13.208866665795702,  75.20913323175502],
  [ 13.208930295699284,  75.20938872633347],
  [ 13.208924511167249,  75.20961649282661],
  [ 13.208824245861251,  75.20992744357834],
  [ 13.208714339613136,  75.2100660840409],
  [ 13.208656494197395,  75.21042060754411],
  [ 13.208743262312694,  75.2107889950589],
  [ 13.208791205887529,  75.21102057042617],
  [ 13.208764211371385,  75.21125625921252],
  [ 13.208704437783792,  75.21144045299835],
  [ 13.207927379880378,  75.21206433509268],
  [ 13.207819401411426,  75.21223466482135],
  [ 13.207763483973508,  75.21251590690254],
  [ 13.207805797250295,  75.21281355066962],
  [ 13.208029466886417,  75.21321164685499],
  [ 13.208347617316985,  75.21330473404275],
  [ 13.208700474586257,  75.21333444271703],
  [ 13.2090096824253,  75.21353680461323]]
const markers10 = [[ 13.2090096824253,  75.21353680461323], 
  [ 13.209078654241063,  75.2136038164443],
  [ 13.20967222541243,  75.21379123487117],
  [ 13.209880090460473,  75.21410438970146],
  [ 13.209903186566011,  75.21437958637051],
  [ 13.20975730013822,  75.21477572791729],
  [ 13.209484765790917,  75.21513158567898],
  [ 13.20914294262007,  75.2154874434407],
  [ 13.208826524794544,  75.21629642680529],
  [ 13.208630206960775,  75.21837463622126],
  [ 13.208697186003702,  75.21867355674108],
  [ 13.208787261239394,  75.21878980360991],
  [ 13.209011294373733,  75.21889181616835],
  [ 13.209226088835244,  75.21904364881334],
  [ 13.209366975422412,  75.21924530154497],
  [ 13.20930923502959,  75.21976248153311],
  [ 13.20922146960342,  75.22000683719614],
  [ 13.209200683050375,  75.22055011341006],
  [ 13.209335109568045,  75.22119506852151],
  [ 13.209360789506652,  75.22146822096458]]
const markers11 = [[ 13.209360789506652,  75.22146822096458], 
  [ 13.209374373033796,  75.2216481940714],
  [ 13.209284298014765,  75.22245480499792],
  [ 13.209150340227003,  75.22275135318681],
  [ 13.207810758333798,  75.22428154164251],
  [ 13.207226421183737,  75.22485091406124],
  [ 13.206976980393355,  75.2254368931755],
  [ 13.206935406895203,  75.22624824894338],
  [ 13.207083223715825,  75.2264712531407],
  [ 13.207635407351582,  75.22691280169694],
  [ 13.208034973343132,  75.22750352558137],
  [ 13.208353094835891,  75.2284386938098],
  [ 13.208342005662713,  75.22902731761222],
  [ 13.208455155125018,  75.22930231931599]]
const markers12 = [[ 13.208455155125018,  75.22930231931599], 
  [ 13.208627176263995,  75.23009804195601],
  [ 13.208791159414485,  75.23087143954015],
  [ 13.20913529269564,  75.23146690819473],
  [ 13.211094856086119,  75.23253904991675],
  [ 13.212695403093894,  75.23326025500819],
  [ 13.212854764339253,  75.23371812532824],
  [ 13.212191913251614,  75.23528389955987],
  [ 13.212157269416707,  75.23577023853353],
  [ 13.212175201036517,  75.23598577559122]]
const markers13 =  [[ 13.212175201036517,  75.23598577559122], 
  [ 13.212312011838227,  75.23623285362376],
  [ 13.212629410575076,  75.23668090758837],
  [ 13.212495454625316,  75.23771526754211],
  [ 13.212246952693992,  75.2380151318549],
  [ 13.211847393597196,  75.2383045628344],
  [ 13.211383165144643,  75.23849198127704],
  [ 13.209322996395898,  75.23992490193436],
  [ 13.208583918163049,  75.24056307356075],
  [ 13.208583918163049,  75.24056307356075],
  [ 13.207610822217017,  75.24272361551832],]
const markers14 =  [[ 13.207610822217017,  75.24272361551832], 
  [ 13.207422175048164,  75.2433174126958],
  [ 13.206942968710647,  75.24785755879765],
  [ 13.20692680124096,  75.24853606092995],
  [ 13.207180861356647,  75.24984798993702],
  [ 13.207026115680897,  75.25067832477392],
  [ 13.20642373534999,  75.25166255936001]]
const markers15 = [[ 13.20642373534999,  75.25166255936001], 
  [ 13.20632398481252,  75.2519333165187],
  [ 13.206155380714652,  75.25246947558334],
  [ 13.206155380714652,  75.25246947558334],
  [ 13.206645136254972,  75.2548995382865],
  [ 13.206943079817334,  75.25509881865005],
  [ 13.207305692784475,  75.25512728727101],
  [ 13.207719117102712,  75.25499680609171],
  [ 13.20843048246556,  75.25452707384105],
  [ 13.208672992925148,  75.2544748813647],
  [ 13.209733107175387,  75.25473347134223],
  [ 13.210160385040739,  75.25479278097255],
  [ 13.21138447423576,  75.2547453332696],
  [ 13.21205068516866,  75.25454984089461]]
const markers16 = [[ 13.21205068516866,  75.25454984089461], 
  [ 13.212105067256958,  75.25454842530813],
  [ 13.21370560764529,  75.25382010305312],
  [ 13.214155974257801,  75.25394346708015],
  [ 13.215047466743497,  75.25485683537501],
  [ 13.215423925038094,  75.25498731658584],
  [ 13.217253088294738,  75.25538824967126],
  [ 13.21785650257807,  75.25604910517373],
  [ 13.217877288402056,  75.25672523494273],
  [ 13.217581667746865,  75.25697196299085],
  [ 13.216967289846933,  75.25704488550188],
  [ 13.216272243753368,  75.2569513055011]]
const markers17 = [[ 13.216272243753368,  75.2569513055011], 
  [ 13.215714057749452,  75.25698955232991],
  [ 13.212436776494112,  75.25828961942379],
  [ 13.211593775969526,  75.25857193325349],
  [ 13.21104409186322,  75.25889932241648],
  [ 13.210778487749323,  75.25930500027246],
  [ 13.210801583769838,  75.25983166975978],
  [ 13.2115776088012,  75.26111987493017],
  [ 13.211967929984034,  75.26143777453693],
  [ 13.212373922603481,  75.26157104785175]]
const markers18 = [[ 13.212373922603481,  75.26157104785175], 
  [ 13.212355940957195,  75.26155639379812],
  [ 13.212746260904702,  75.26161333104099],
  [ 13.213764785119812,  75.26156351095435],
  [ 13.21450743510889,  75.26185185492693],
  [ 13.214604436898133,  75.26227413947082],
  [ 13.214355003647853,  75.26307126085702],
  [ 13.214066307432939,  75.26326342406291],
  [ 13.213687537479448,  75.26340102239574],
  [ 13.212188618915883,  75.26352913121025],
  [ 13.211585815478216,  75.26379721073721],
  [ 13.211343307926658,  75.26434997648803],
  [ 13.212117561916477,  75.2664455344316]]
const markers19 = [[ 13.212117561916477,  75.2664455344316], 
  [ 13.212274073680312,  75.26672947882857],
  [ 13.214084531212016,  75.27013020315857],
  [ 13.214142270477,  75.27092020738954],
  [ 13.213821239981005,  75.27138282253863],
  [ 13.212398538636029,  75.27224399833332],
  [ 13.211156206948843,  75.27377873133574]]
const markers20 = [[ 13.211156206948843,  75.27377873133574], 
  [ 13.21098968657654,  75.27396872236535],
  [ 13.2099318873795,  75.27516440451183],
  [ 13.209666282058835,  75.27601371838875],
  [ 13.207973330066965,  75.2782366432867],
  [ 13.206275747036404,  75.2795390827761],
  [ 13.205968564076516,  75.28012506191332],
  [ 13.205903519459017,  75.28094305301288]]
const markers21 = [[ 13.205903519459017,  75.28094305301288], 
  [ 13.205908513229781,  75.28110248456547],
  [ 13.206701621484916,  75.28497355288538],
  [ 13.20708502155549,  75.28702329366679],
  [ 13.20696917049813,  75.28810867479216],
  [ 13.206754374050872,  75.28862348235408],
  [ 13.20640561811948,  75.28894612673261],
  [ 13.205622072528882,  75.28930667573731]]
const markers22 = [[ 13.205622072528882,  75.28930667573731], 
  [ 13.204938990046626,  75.2898357711767],
  [ 13.20473804976965,  75.29031736534753],
  [ 13.204742669085734,  75.29104331522802],
  [ 13.20492744175684,  75.29143950353604],
  [ 13.206387140958373,  75.29236236134916],
  [ 13.208462179456506,  75.29320064333835],
  [ 13.208804003580614,  75.29385067684973],
  [ 13.208767049646209,  75.29517209539087],
  [ 13.208648306591009,  75.29571248943518]]
const markers23 = [[ 13.208648306591009,  75.29571248943518], 
  [ 13.208429844709563,  75.29635117084676],
  [ 13.208332840466193,  75.29685648886837],
  [ 13.208385961842337,  75.2975017776096],
  [ 13.20868852250713,  75.29808301201294],
  [ 13.209067300220742,  75.2983178781447],
  [ 13.209492395893509,  75.2984331619927],
  [ 13.210439335953058,  75.29857550510603],
  [ 13.210744203671483,  75.29880562645859],
  [ 13.211307746034985,  75.29961223739717],
  [ 13.21288161103287,  75.30033864116537],
  [ 13.214006375011996,  75.3004857290408],
  [ 13.21453625854513,  75.30031505813517]]
const markers24 = [[ 13.21453625854513,  75.30031505813517], 
  [ 13.215216587557766,  75.30013936082435],
  [ 13.215874811335086,  75.30017020182136],
  [ 13.216655439326301,  75.30095071651914],
  [ 13.217207420336653,  75.30228874173216],
  [ 13.217798662207743,  75.30268493007932],
  [ 13.220181191926955,  75.3031278182196],
  [ 13.221634646620192,  75.30365055598062],
  [ 13.222051341483827,  75.30381564354727]]
const markers25 =  [[ 13.222051341483827,  75.30381564354727], 
  [ 13.22263031687889,  75.30426519181263],
  [ 13.223200760244575,  75.30539207474392],
  [ 13.224103767060283,  75.30903843078372],
  [ 13.226013195220197,  75.31091604765581],
  [ 13.22633959984309,  75.31158104684977]]
const markers26 = [[ 13.22633959984309,  75.31158104684977], 
  [ 13.226357304211064,  75.31133358748602],
  [ 13.226278782740035,  75.31214257079762],
  [ 13.225699108744955,  75.3124248846219],
  [ 13.224163312376971,  75.31237269215107],
  [ 13.223521277345485,  75.3125862068138],
  [ 13.222761456725038,  75.31304644955793],
  [ 13.222251059183927,  75.31351618180338],
  [ 13.222110180025046,  75.31412114003984],
  [ 13.222227964241887,  75.31480913174408],
  [ 13.22278254396042,  75.3153991029294],
  [ 13.224048181997974,  75.3161253141576],
  [ 13.224559104069446,  75.31623513670458]]
const markers27 = [[ 13.224559104069446,  75.31623513670458], 
  [ 13.225141192271645,  75.31627891247764],
  [ 13.22711058325138,  75.31617044401976],
  [ 13.228585480913933,  75.31668181674928],
  [ 13.229354521077914,  75.31759044025694],
  [ 13.229813083979293,  75.31981368432668],
  [ 13.22970454112566,  75.32055149612347]]

const pathOptions = {
  strokeColor: '#FF0000',
  strokeOpacity: 0.5,
  strokeWeight: 2,
  fillColor: '#FF0000',
  fillOpacity: 0.5,
  clickable: false,
  geodesic: true,
  zIndex: 2
};

const getMapOptions = (maps) => {
  return {
    disableDefaultUI: true,
    mapTypeControl: true,
    streetViewControl: false,
    zoomControl: true,
    mapTypeControlOptions: {
      mapTypeIds: [
          maps.MapTypeId.TERRAIN
      ]
  },
    styles: [{ featureType: 'poi', elementType: 'labels', stylers: [{ visibility: 'on' }] }],
  };
};

const locations=['locationA','locationB']

class Map extends React.Component {
    // console.log(location)
    constructor(props){
        super(props);
        this.state={rows:[],
                    rows1:[],
                    mapsLoaded: false,
                    map: null,
                    maps: null,
                    selected_map:1,
                    layer:1,
                    marker:1,
                    colour1: "blue",
                    colour2: "blue",
                    colour3: "blue",
                    colour4: "blue",
                    river_location: null,
                    river_est_location: null,
                    Est_mark: "Add Estimated Markers",
                  };
        this.onChangeValue = this.onChangeValue.bind(this);
        this.onChangeValue1 = this.onChangeValue1.bind(this);
        this.onChangeValue2 = this.onChangeValue2.bind(this);
        this.changeColour = this.changeColour.bind(this);
        this.changeText = this.changeText.bind(this);
        
        this.colourid_1 = React.createRef();
        this.colourid_2 = React.createRef();
        this.colourid_3 = React.createRef();
        this.colourid_4 = React.createRef();
        this.colourid_5 = React.createRef();

                }
    async getData(){
        const response = await axios.get(`https://localhost:5000/check`)
        return await response.data;
    }
    onMapLoaded (map, maps) {
    this.fitBounds(map, maps)

    this.setState({
      mapsLoaded: true,
      map: map,
      maps: maps
    })
  }
  fitBounds (map, maps) {
    var bounds=new maps.LatLngBounds()
    for (let marker of this.props.markers) {
      bounds.extend(
        new maps.LatLng(marker.lat, marker.lng)
      )
    }
    map.fitBounds(bounds)
  }
  initialColor = () => {
    this.colourid_1.current.value="#08DCF1"
    this.colourid_2.current.value="#0887F1"
    this.colourid_3.current.value="#F18E08"
    this.colourid_4.current.value="#F15D08"
    this.colourid_5.current.value="#B64444"

 }
  afterMapLoadChanges () {
    return (
      <div style={{display: 'none'}}>
        <Polyline
          map={this.state.map}
          maps={this.state.maps}
          markers={this.props.markers}
          markers1={this.props.markers1}
          markers2={this.props.markers2}
          markers3={this.props.markers3}
          markers4={this.props.markers4}
          markers5={this.props.markers5}
          markers6={this.props.markers6}
          markers7={this.props.markers7}
          markers8={this.props.markers8}
          markers9={this.props.markers9}
          markers10={this.props.markers10}
          markers11={this.props.markers11}
          markers12={this.props.markers12}
          markers13={this.props.markers13}
          markers14={this.props.markers14}
          markers15={this.props.markers15}
          markers16={this.props.markers16}
          markers17={this.props.markers17}
          markers18={this.props.markers18}
          markers19={this.props.markers19}
          markers20={this.props.markers20}
          markers21={this.props.markers21}
          markers22={this.props.markers22}
          markers23={this.props.markers23}
          markers24={this.props.markers24} 
          markers25={this.props.markers25}
          markers26={this.props.markers26}
          markers27={this.props.markers27}
          res={this.state.rows1}
          />
      </div>
    )
  }
    componentDidMount(){
      this.initialColor();
      console.log(this.colourid_1.current.value)

        var row=[]
        var row1=[]
        var res={}
        axios({
            method: 'get',
            url: 'https://hydrologytool-backend.herokuapp.com/'
        })
        .then(resData=>resData.data)
        .then(res => {
        for (var i=0;i<res.river_locations.length;i++){
          console.log(this.props.locationselect[locations[i]])
          if (this.props.locationselect[locations[i]]==true){
            row.push((<Marker 
            lat={res.river_locations[i].lat}
            lng={res.river_locations[i].lng}
            name="My marker"
            color={res.river_locations[i].color}
            />))
          }
        }
        this.setState({rows:row});
       

      });

    axios({
            method: 'get',
            url: 'http://localhost:5000/check'
        })
        .then(resData=>resData.data)
        .then(res => {
            console.log(res);
        
        for (var i=0;i<res.river_locations.length;i++){
            row1.push(<Marker 
            lat={res.river_locations[i].lat}
            lng={res.river_locations[i].lng}
            name="My marker"
            color={res.river_locations[i].color}
            />)  
        }
        this.setState({rows1:row1}); 
    });
    console.log("get data");

    // backend data---------------------------------------------------------------------------------------
    axios.get('http://127.0.0.1:5000/getdata')
			.then(res => {
					console.log(res);
					this.setState({
						river_location: res.data,
					})
			})
      axios.get('http://127.0.0.1:5000/getEstdata')
			.then(res => {
					console.log(res);
					this.setState({
						river_est_location: res.data,
					})
			})
}



onChangeValue(event) {
  var data1= (event.target.value);
  this.setState({ selected_map: data1 }); 
}

onChangeValue1(event) {
  var data1= (event.target.value);
  this.setState({ layer: data1 }); 
}

onChangeValue2(event) {
  var data2= (event.target.value);
  this.setState({ marker: data2 }); 
}


changeColour() {
  this.setState({ 
    colour1: this.colourid_1.current.value,  
    colour2: this.colourid_2.current.value,  
    colour3: this.colourid_3.current.value,
    colour4: this.colourid_4.current.value
  }); 
  console.log(this.state.colour1);
  console.log(this.colourid_1.current.value);
}

changeText = () => {
  if(this.state.Est_mark =="Add Estimated Markers"){
    this.setState({ Est_mark: "Remove Estimated Markers"});  
  }
  else{
  this.setState({ Est_mark: "Add Estimated Markers"}); }
}




    render(){
    const isLoggedIn=this.props.submit;  
    
    console.log(this.state.colour1);
    console.log("Hii");
    console.log(this.state.river_location);
    if(this.state.selected_map==1 || this.state.selected_map==3){
      

    return (<div className="map" style={{ height: '83vh', width: '100%' }}>  
      <pre>
      
       
         
        Excellent:
        <input ref= {this.colourid_1} name="MyColorPicker" type="color"   />
        .       Good:
        <input ref= {this.colourid_2} name="MyColorPicker" type="color"  />
        .       Poor:
        <input ref= {this.colourid_3} name="MyColorPicker" type="color"  />
        .       Very Poor:
        <input ref= {this.colourid_4} name="MyColorPicker" type="color"  />
        .       Unsuitable:
        <input ref= {this.colourid_5} name="MyColorPicker" type="color"  />
        {/* <label>Please pick any colour and click this submit button </label> */}
        <ThemeProvider theme={theme}><Button variant="contained" color='neutral' style={{ margintop: -80, marginLeft : 50 }} onClick={this.changeColour}>Submit</Button></ThemeProvider>
        <br></br> 
        </pre>

        <LeafletMap data={this.state.river_location} Estdata={this.state.river_est_location} text={this.state.Est_mark} tilelayer={this.state.selected_map} layer={this.state.layer} marker={this.state.marker} colour_1={this.state.colour1}  colour_2={this.state.colour2}  colour_3={this.state.colour3} colour_4={this.state.colour4}/>

   

    </div>);

    }
  
  
  else if (this.state.selected_map==2 && this.state.layer==1) {
    return (  
      <div>
        <div onChange={this.onChangeValue}>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="maps" value="1"></input>
          <label class="form-check-label" for="inlineRadio3">Street map</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="maps" value="2" checked></input>
          <label class="form-check-label" for="inlineRadio1">Physical Map</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="maps" value="3"></input>
          <label class="form-check-label" for="inlineRadio2">None</label>
        </div>
      </div>
      <div onChange={this.onChangeValue1}>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="Baselayer" value="1" checked></input>
          <label class="form-check-label" for="inlineRadio3">With layer</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="Baselayer" value="0"></input>
          <label class="form-check-label" for="inlineRadio1">Without layer</label>
        </div>
      </div>
      <MapContainer center={center} zoom={16} scrollWheelZoom={false}>
        
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={center}>
          <Popup>
            Start Point of Bhadra. <br /> 
          </Popup>
        </Marker>
        <Polyline pathOptions={limeOptions} positions={markers} />
      
        <Polyline pathOptions={limeOptions} positions={markers1} />
        <Polyline pathOptions={limeOptions} positions={markers2} />
        <Polyline pathOptions={limeOptions} positions={markers3} />
        <Polyline pathOptions={limeOptions} positions={markers4} />
        <Polyline pathOptions={limeOptions} positions={markers5} />
        <Polyline pathOptions={limeOptions} positions={markers6} />
        <Polyline pathOptions={limeOptions} positions={markers7} />
        <Polyline pathOptions={limeOptions} positions={markers8} />
        <Polyline pathOptions={limeOptions} positions={markers9} />
        <Polyline pathOptions={limeOptions} positions={markers10} />
        <Polyline pathOptions={limeOptions} positions={markers11} />
        <Polyline pathOptions={limeOptions} positions={markers12} />
        <Polyline pathOptions={limeOptions} positions={markers13} />
        <Polyline pathOptions={limeOptions} positions={markers14} />
        <Polyline pathOptions={limeOptions} positions={markers15} />
        <Polyline pathOptions={limeOptions} positions={markers16} />
        <Polyline pathOptions={limeOptions} positions={markers17} />
        <Polyline pathOptions={limeOptions} positions={markers18} />
        <Polyline pathOptions={limeOptions} positions={markers19} />
        <Polyline pathOptions={limeOptions} positions={markers20} />
      </MapContainer>
        </div>  )
          ;
  }
  else if (this.state.selected_map==2 && this.state.layer==0) {
    return (  
      <div>
        <div onChange={this.onChangeValue}>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="maps" value="1"></input>
          <label class="form-check-label" for="inlineRadio3">Street map</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="maps" value="2" checked></input>
          <label class="form-check-label" for="inlineRadio1">Physical Map</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="maps" value="3"></input>
          <label class="form-check-label" for="inlineRadio2">None</label>
        </div>
      </div>
      <div onChange={this.onChangeValue1}>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="Baselayer" value="1"></input>
          <label class="form-check-label" for="inlineRadio3">With layer</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="Baselayer" value="0" checked></input>
          <label class="form-check-label" for="inlineRadio1">Without layer</label>
        </div>
      </div>
      <MapContainer center={center} zoom={16} scrollWheelZoom={false}>
        
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
      </MapContainer>
        </div>  )
          ;
  }
    else
    {
      return (<div className="map" style={{ height: '83vh', width: '100%' }}>  
          <div onChange={this.onChangeValue}>
          <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="maps" value="1"></input>
          <label class="form-check-label" for="inlineRadio3">Street map</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="maps" value="2"></input>
          <label class="form-check-label" for="inlineRadio1">Physical Map</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="maps" value="3"></input>
          <label class="form-check-label" for="inlineRadio2">None</label>
        </div>
      </div>
      <div onChange={this.onChangeValue1}>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="Baselayer" value="1"></input>
          <label class="form-check-label" for="inlineRadio3">With layer</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="Baselayer" value="0"></input>
          <label class="form-check-label" for="inlineRadio1">Without layer</label>
        </div>
      </div>

    <h1>Some Error please Check</h1>
    </div>);

    }
    }
}
export default Map;


