function displaycard(display_name, id, download = true, url = ""){
    this.display_name = display_name;
    this.url = url;
    this.sample_list = [];
    this.card_id = id;
};

function datasample(dataset_name, type, id, pic_url, annotation){
    this.dataset_name = dataset_name;
    this.pic_id = id;
    this.pic_url = pic_url;
    this.annotation = annotation;
    this.type = type;
    this.get_image_thumbnail = function(){
        var part1 = '<div class="col-xs-12 col-sm-6 col-md-4" style="margin-top: 0.5rem; margin-bottom: 0.5rem">'+
                    '<div class="thumbnail">'+
                    '<a href="'+this.pic_url+'" target="_blank">'+
                    '<img src="'+this.pic_url+'" width="100%">'+
                    '</a>'+
                    '</div>'+
                    '</div>'; 
       return part1;
    }
}

