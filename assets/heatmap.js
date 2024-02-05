L.Control.Fullscreen = L.Control.extend({
    onAdd: function() {
        var controlDiv = L.DomUtil.create('div');
        controlDiv.className = 'fullscreen';
        return controlDiv;
    },
    onRemove: function() {},
    _onKeyDownHandler: function(event) {
        if (!this._map || event.altKey || event.ctrlKey || event.metaKey) return true;
        switch (String.fromCharCode(event.which).toLowerCase()) {
            case 'f':
                this._map.toggleFullscreen();
                break;
        }
        return false;
    }
});

L.control.fullscreen = function(opts) {
    return new L.Control.Fullscreen(opts);
};