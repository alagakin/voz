import {Marker} from 'leaflet';

class CustomMarker extends Marker {
    constructor(latlng, options) {
        super(latlng, options);

        // Add custom initialization logic here
    }
    _setPos(pos) {
        super._setPos(pos)
        this._icon.style.transform += " rotate(" + this.options.rotation + "deg)"
        this._icon.style.transformOrigin = "center center"
    }

}

function marker(latlng, options) {
    return new CustomMarker(latlng, options);
}

export default marker
