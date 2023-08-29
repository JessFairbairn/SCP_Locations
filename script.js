console.log("running")
let site_list;

const listMarkerMap = new WeakMap();

fetch("site_locations.json").then(resp => resp.json()).then(payload => {
    site_list = payload;
    const list_element = document.getElementById("site-list");
    for (let site of site_list) {
        if (site["lat"] === undefined || site["long"] === undefined) {
            continue;
        }

        let listItem = document.createElement("li");
        listItem.innerText = site["site long name"];
        list_element.appendChild(listItem);


        let marker = L.marker([site.lat, site.long]).addTo(map);
        marker.bindPopup(`${site["site long name"]}, ${site["location name"]}
        <br/><i>${site.sentence}</i>
        <br>from <a href="https://www.scp-wiki.net/${site["page name"]}">${site["page name"]}</a>`)

        listItem.onclick = () => {
            marker.openPopup();
            map.flyTo(marker.getLatLng(), 7);
        }
    }
})


// set up map
const map = L.map('map').setView([51.505, -0.09], 2);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    minZoom: 1,
    attribution: '© OpenStreetMap'
}).addTo(map);

// const cluster = L.markerCluster().addTo(map);

const TOGGLE_LIST_BUTTON = document.getElementById("toggle-button")
TOGGLE_LIST_BUTTON.onclick = () => 
    document.getElementById("site-list").classList.toggle("collapsed");
