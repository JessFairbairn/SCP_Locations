console.log("running")
document.getElementById('testBtn').onclick= () => {
    const mapWindow = document.getElementById('mapFrame').contentWindow;
    let keys = Object.keys(mapWindow);
    let mapObjKey = keys.filter( name => name.startsWith("map_"))[0];
    const mapObj = mapWindow[mapObjKey];
    mapObj.zoomIn();
};
