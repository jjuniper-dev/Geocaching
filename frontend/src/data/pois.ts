import type { POI } from '../types/geospatial'

const pois: POI[] = [
  {
    id: 'pink-lake',
    name: 'Pink Lake',
    type: 'wildlife',
    coordinates: [45.4564, -75.7925],
    description:
      'A meromictic lake — its layers never mix, preserving ancient sediment records dating back 11,000 years. The green-blue colour comes from a unique balance of bacteria and the lack of oxygen in lower depths.',
    conservation:
      'Fencing protects the shoreline. Stay on the boardwalk — bank erosion threatens the stratification.',
    source: 'Parks Canada / NCC',
  },
  {
    id: 'champlain-lookout',
    name: 'Champlain Lookout',
    type: 'scenic',
    coordinates: [45.4887, -75.9221],
    description:
      'The most panoramic viewpoint in Gatineau Park. On clear days you can see the Ottawa River valley and the Laurentian highlands. Part of the Canadian Shield edge, this escarpment was formed over a billion years ago.',
    source: 'NCC Gatineau Park',
  },
  {
    id: 'lusk-cave',
    name: 'Lusk Cave',
    type: 'trail',
    coordinates: [45.5372, -75.9116],
    description:
      'A 100-metre marble cave accessible via an 11 km round-trip trail. Wading through an underground stream is part of the experience. Bring a headlamp — no lighting inside.',
    conservation:
      'Do not disturb hibernating bats (November–April). White-nose syndrome threatens local bat populations.',
    season: 'Best: May–October. Trail closed during winter.',
    source: 'NCC Gatineau Park',
  },
  {
    id: 'mackenzie-king-estate',
    name: 'Mackenzie King Estate',
    type: 'historical',
    coordinates: [45.4741, -75.8512],
    description:
      "Canada's longest-serving Prime Minister used this retreat from 1903 until his death in 1950. The estate features ruins he collected from Britain, formal gardens, and three restored cottages with original furnishings.",
    season: 'Open May–October. Tea room on site.',
    source: 'NCC / Parks Canada',
  },
  {
    id: 'carbide-willson-ruins',
    name: 'Carbide Willson Ruins',
    type: 'historical',
    coordinates: [45.4582, -75.7965],
    description:
      "Dramatic stone ruins of Thomas Willson's 1900s experimental calcium carbide laboratory on the shores of Meech Creek. Willson invented the industrial production of calcium carbide here — a precursor to acetylene gas technology.",
    conservation:
      'Ruins are structurally fragile. Do not climb on the walls.',
    source: 'NCC Gatineau Park',
  },
  {
    id: 'meech-lake',
    name: 'Meech Lake',
    type: 'scenic',
    coordinates: [45.4989, -75.8699],
    description:
      'A pristine lake inside Gatineau Park with a public beach, canoe rentals, and calm water ideal for swimming. Named after Methodist minister Reverend Asa Meech who settled here in 1823.',
    season: 'Swimming season: June–August.',
    source: 'NCC Gatineau Park',
  },
  {
    id: 'skyline-trail',
    name: 'Skyline Trail',
    type: 'trail',
    coordinates: [45.4962, -75.8920],
    description:
      'A moderately challenging ridge trail offering continuous views westward across the Gatineau Hills. The rocky Canadian Shield terrain is typical of the Precambrian highlands that define this region.',
    source: 'NCC Gatineau Park',
  },
  {
    id: 'king-mountain',
    name: 'King Mountain Viewpoint',
    type: 'scenic',
    coordinates: [45.4695, -75.8099],
    description:
      'A rocky summit accessible via a short but steep trail, offering close-up views of the Ottawa Valley farmland below. The summit granite is some of the oldest exposed rock in the region — over 1 billion years old.',
    source: 'NCC Gatineau Park',
  },
  {
    id: 'etienne-brule-lookout',
    name: 'Étienne Brûlé Lookout',
    type: 'scenic',
    coordinates: [45.4879, -75.8944],
    description:
      "Named for Champlain's interpreter who explored this region in the early 1600s. The lookout gives a sweeping view over the Ottawa River and Outaouais region. One of the quieter viewpoints in the park.",
    source: 'NCC Gatineau Park',
  },
  {
    id: 'camp-fortune',
    name: 'Camp Fortune',
    type: 'trail',
    coordinates: [45.5009, -75.8489],
    description:
      'A four-season outdoor recreation area. In winter, it operates as a ski hill. In summer and fall, it becomes a hub for mountain biking, zip-lining, and trail access into the central park network.',
    source: 'Chelsea, QC',
  },
  {
    id: 'chelsea-pub',
    name: 'The Chelsea Pub',
    type: 'food',
    coordinates: [45.5172, -75.7884],
    description:
      'A beloved village institution in Old Chelsea. Solid pub food, local craft beers, a log-cabin feel, and a lively patio. Hikers from Gatineau Park frequently end their day here. First opened in the 1980s.',
    source: 'Old Chelsea, QC',
  },
  {
    id: 'la-cigale',
    name: 'La Cigale',
    type: 'food',
    coordinates: [45.5175, -75.7875],
    description:
      'Chelsea\'s warmly regarded neighbourhood restaurant — seasonal menus, strong local ingredients, and a cozy room. A reliable choice for a proper meal before or after exploring the park.',
    source: 'Old Chelsea, QC',
  },
  {
    id: 'wakefield-village',
    name: 'Wakefield Village',
    type: 'cultural',
    coordinates: [45.6351, -75.8335],
    description:
      'A small arts village straddling the Gatineau River, 30 km north of Chelsea. Known for its covered bridge, the Black Sheep Inn music venue, artisan studios, and the historic steam train that once ran here.',
    source: 'Wakefield, QC',
  },
  {
    id: 'black-sheep-inn',
    name: 'Black Sheep Inn',
    type: 'cultural',
    coordinates: [45.6353, -75.8329],
    description:
      'A legendary small live-music venue that has hosted Canadian and international folk, jazz, and roots artists for over 30 years. The intimate room seats under 100 people. Reservations essential.',
    source: 'Wakefield, QC',
  },
  {
    id: 'lac-la-peche',
    name: 'Lac La Pêche',
    type: 'wildlife',
    coordinates: [45.5724, -75.9527],
    description:
      'A remote wilderness lake in the western backcountry of Gatineau Park. Accessible by an 8 km trail or canoe portage. Canoe camping is permitted here — one of the few places in the park for it.',
    conservation:
      'Carry-in, carry-out rules apply. No motorized watercraft permitted.',
    season: 'Access May–October only.',
    source: 'NCC Gatineau Park',
  },
  {
    id: 'herridge-shelter',
    name: 'Herridge Shelter',
    type: 'trail',
    coordinates: [45.5181, -75.8943],
    description:
      'A backcountry lean-to accessible via multiple trail routes. A useful navigation landmark and rest point in the central park network. The surrounding boreal-transitional forest is typical of the Gatineau highland interior.',
    source: 'NCC Gatineau Park',
  },
  {
    id: 'gatineau-visitor-centre',
    name: 'Gatineau Park Visitor Centre',
    type: 'scenic',
    coordinates: [45.4625, -75.7810],
    description:
      'The main entry point for park information, trail maps, and seasonal programming. Staff can advise on current trail conditions, wildlife activity, and conservation events. Good starting point for first-time visitors.',
    source: 'NCC Gatineau Park',
  },
  {
    id: 'sugarbush-trail',
    name: 'Sugarbush Heritage Trail',
    type: 'cultural',
    coordinates: [45.4897, -75.8601],
    description:
      'A 6 km interpretive trail through old maple groves used for syrup production since Indigenous times. Interpretive signs explain the ecology of the sugar maple forest and the history of maple harvesting in the Outaouais.',
    season: 'Sugarbush season: late February–April.',
    source: 'NCC Gatineau Park',
  },
  {
    id: 'philippe-lake',
    name: 'Philippe Lake Campground',
    type: 'scenic',
    coordinates: [45.5456, -75.9301],
    description:
      'A well-maintained NCC campground on a large lake in the western park. Canoe and kayak rentals available. The lake is bordered by mixed boreal forest and offers quieter conditions than busier areas near Chelsea.',
    season: 'Camping season: May–October.',
    source: 'NCC Gatineau Park',
  },
  {
    id: 'old-chelsea-cemetery',
    name: 'Old Chelsea Cemetery',
    type: 'historical',
    coordinates: [45.5174, -75.7878],
    description:
      "A historic rural cemetery in the heart of Old Chelsea, with graves dating to the early 1800s. The headstones document the community's early settler families — Irish, Scottish, and English immigrants who cleared this land.",
    source: 'Chelsea, QC Heritage Registry',
  },
]

export default pois
