console.log("running")
document.getElementById('testBtn').onclick= () => {
    const mapWindow = document.getElementById('mapFrame').contentWindow;
    let keys = Object.keys(mapWindow);
    let mapObjKey = keys.filter( name => name.startsWith("map_"))[0];
    const mapObj = mapWindow[mapObjKey];
    mapObj.zoomIn();
};

let site_list;

fetch("site_locations.json").then(resp => resp.json()).then(payload => {
    site_list = payload;
    const list_element = document.getElementById("site-list");
    for (let site of site_list) {
        let listItem = document.createElement("li");
        listItem.innerText = site["site long name"];
        list_element.appendChild(listItem);
    }
})
