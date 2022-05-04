ymaps.ready(init);

let center = [59.93000542187484,30.35492705654526];

function init() {
	var map = new ymaps.Map("map", {
		center: center,
		zoom: 18
    });

    let placemark = new ymaps.Placemark(center, {}, {});

    map.geoObjects.add(placemark);
}
