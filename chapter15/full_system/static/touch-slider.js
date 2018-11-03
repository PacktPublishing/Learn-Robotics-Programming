
function Slider(id, when_updated) {
    this.selector = '#'  + id;
    this.when_updated = when_updated;
};

Slider.prototype = {
    touched: false,
    direction : 0,
    position : 50,
    when_updated: null,
    changed: false,
    update_if_changed: function() {
        if(this.changed) {
            this.changed = false;
            this.when_updated(100 - this.position * 2);
            $(this.selector).find('.slider_tick')[0].setAttribute('cy', this.position + '%');
        }
    },
    set_position: function(new_position) {
        this.position = Math.round(new_position);
        console.log(this.id + " - " + this.position);
        this.changed = true;
    },
    update : function() {
        this.direction = 50 - this.position;
        this.direction = Math.ceil(Math.abs(0.3 * this.direction) + 0.7) * Math.sign(this.direction)
        if(!this.touched && this.position != 50) {
            this.set_position(this.position + this.direction);
        }
    },
    setup: function() {
        setInterval(this.update.bind(this), 50);
        setInterval(this.update_if_changed.bind(this), 200);
        $(this.selector).on('touchmove', function(event) {
            var touch = event.targetTouches[0];
            //height of track in pixels
            //set current_position to touch position relative to top of track, as percentage of track.
            var tracktop = $(this.selector).offset().top;
            var trackheight =  $(this.selector).height();
            var relative_touch = Math.round(((touch.pageY - tracktop)/trackheight) * 100);
            relative_touch = Math.max(0, Math.min(100, relative_touch));
            this.set_position(relative_touch);
            this.touched = true;
            event.preventDefault();
        }.bind(this));
        $(this.selector).on('touchend', function(event) {
            this.touched = false;
        }.bind(this));
    }
}
document.write("v2s");
