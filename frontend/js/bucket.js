function Barrels($ct, imgUrls, Height) { 
  this.$ct = $ct;
  this.imgNum = 40; 
  this.baseHeight = Height;
  this.rowList = [];
  this.loadImg(imgUrls);
}
Barrels.prototype = {
  loadImg: function(imgUrls) {
    var _this = this;
    $.each(imgUrls,function(idx, url){
      var img = new Image();
      img.src = url;
      img.onload = function(){
        var originWidth = img.width,
            originHeight = img.height,
            ratio = originWidth/originHeight;
        var imgInfo = {
          target: $(img),
          width: _this.baseHeight*ratio,
          height: _this.baseHeight,
          ratio: ratio
        };
        _this.render(imgInfo);
      };
    });
  },
  render: function(imgInfo){
    var _this = this;
    var rowList = this.rowList,
        rowWidth = 0,
        rowHeight = 0,
        clientWidth = this.$ct.width(),
        lastImgInfo = imgInfo;
    this.rowList.push(imgInfo);
    $.each(rowList,function(idx, imgInfo){
      rowWidth += imgInfo.width;
      if(rowWidth  > clientWidth ){ 
        rowList.pop();
        rowWidth = rowWidth - lastImgInfo.width;
        rowHeight = clientWidth * _this.baseHeight / rowWidth;
        _this.createRow(rowHeight);
        _this.rowList = [];
        _this.rowList.push(lastImgInfo);
      }
    });
  },
  createRow: function(rowHeight){
    var $rowCt = $('<div class="img-row"></div>');
    $.each(this.rowList, function(idx, imgInfo){
      var $imgCt = $('<div class="img-box"></div>'),
          $img = imgInfo.target;
          $img.height(rowHeight);
          $imgCt.append($img);
          $rowCt.append($imgCt);
    });
    this.$ct.append($rowCt);
  }
};