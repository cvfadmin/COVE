gen_displaycard_header = function(card_id, name, download, url){
   var part1 = '<div class="row dataset-row" style="height:230px; margin-bottom: 10px" id="card_' + card_id.toString()+ '">' +
                  '<div class="wrap" style="height:40px; text-align: center; border-bottom: 1px solid #e5e5e5">';
   if(!download){
      part1 += '<div class="left">' + 
                 '<button type="button" class="btn btn-success" style="margin:5px 2px; height: 30px;padding: 2px; float:left" ng-click="add_card_to_download('+card_id+')">Add to download </button>' +
               '</div>'+
               '<div class="right">' +                     
                 '<button type="button" class="close" aria-label="Close" ng-click="delete_card('+ card_id.toString()+')" style="margin-right:0.5rem">' +
                   '<span aria-hidden="true">&times;</span>' +
                 '</button>' +
               '</div>';
   }
   else{
      part1 += '<div class="right">' +                     
                 '<button type="button" class="close" aria-label="Close" ng-click="delete_card('+ card_id.toString()+', true)" style="margin-right:0.5rem; float:right">' +
                   '<span aria-hidden="true">&times;</span>' +
                 '</button>' +
               '</div>';
   }
   if(url != ""){
       part1 +='<div style="margin: auto auto;height : 32px; line-height: 38px">' + '<p style="font-size:32px"> <a href="'+ url + ' " target = "_blank">'+ name + '</a></p>' +
               '</div>' +
                  '</div>'+
               '</div>';
   }
   else{
       part1 +='<div style="margin: auto auto;height : 32px; line-height: 38px">' + '<p style="font-size:32px">'+ name + '</p>' +
               '</div>' +
                  '</div>'+
               '</div>';
   }
   return part1; 
}

gen_expand_button = function(card_id){
  var part1 = '<div style="text-align:center; height:30px">' +
                '<a href="" ng-click="expand('+ card_id.toString() + ')">' +
                  '<span id="dd_icon_'+ card_id.toString()+'" class="octicon octicon-chevron-down" style="height:30px"></span>' +
                '</a>' +
              '</div>';
  return part1;
}


gen_group_button = function(){
  return '<div class="input-group-btn" style = "display: inline-block">' +
                '<button id = "group_button" type="button" class="btn btn-secondary dropdown-toggle"' +
                   'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style = "font-size : 28px; padding : 2px; background-color : rgb(235, 230, 228)">' +
                            'Don\'t group' +
                '</button>' +
                '<div class="dropdown-menu dropdown-menu-right">' +
                    '<a class="dropdown-item" ng-click="group_by_dontgroup()">' +
                        'Don\'t group' +
                    '</a>' +
                    '<a class="dropdown-item" ng-click="group_by_dataset()">'+
                        'Dataset'+
                    '</a>'+
                    '<a class="dropdown-item" ng-click="group_by_annotation()">'+
                        'Annotation'+
                    '</a>'+
                '</div>'+
            '</div>';
}

gen_display_html = function(cur, prev){
  var res = '';
  if(!prev){
    for(var key in cur){
      console.log(key , cur[key]);
    res += '<div class="row" style = "border-bottom: 1pt solid black;">'
     + '<div class="col-sm-2" style = "padding: 5px 0">'
     + key
     + '</div>'
      + '<div class="col-sm-10" style = "padding: 5px 0">'
      + cur[key]
      + '</div>'
      +'</div>'
    }
  }
  else{
    res += '<div class="row" style = "border-bottom: 1pt solid black;">'
     + '<div class="col-sm-2" style = "padding: 5px 0">'
     + '</div>'
      + '<div class="col-sm-5" style = "padding: 5px 0">'
      + 'Previous'
      + '</div>'
      + '<div class="col-sm-5" style = "padding: 5px 0">'
      + 'Current'
      + '</div>'
      +'</div>'
    for(var key in cur){
      res += '<div class="row" style = "border-bottom: 1pt solid black;">'
     + '<div class="col-sm-2" style = "padding: 5px 0">'
     + key
     + '</div>'
      + '<div class="col-sm-5" style = "padding: 5px 0">'
      // + Array.isArray(prev[key]) ? prev[key].join(";") : prev[key]
      + prev[key]
      + '</div>'
      + '<div class="col-sm-5" style = "padding: 5px 0">'
      + cur[key]
      + '</div>'
      +'</div>'
    }
  }
  res += '<div class="row">'
        +'<div class="btn-group" style = "float: right;" role="group" aria-label="Basic example">'
          + '<button type="button" id="dst_approve" class="btn btn-secondary btn-success"  ng-click="dst_approve()">Approve</button>'
          + '<button type="button" id="dst_deny" class="btn btn-secondary btn-danger"  ng-click="dst_deny()">Decline</button>'
        + '</div>'
        + '</div>'
  return res;
}
gen_request_html = function(type, data, id){
  var res = '';
  if(type == 'add'){
    res = '<div class="container-fluid" style = "border-bottom-width:2px; border-bottom-color:Grey; border-bottom-style: solid; width:95%">'
     + '<div class="row">'
     + '<div class="col-sm-2" style = "padding: 5px 0">'
     + 'First Name:'
     + '</div>'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
      + data['firstname']
      + '</div>'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Last Name:'
      + '</div>'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        +data['lastname']
      +'</div>'
      + '<div class="col-sm-4" style = "padding: 5px 0">'
      + '<div class="btn-group" style = "float: right;" role="group" aria-label="Basic example">'
          + '<button type="button" class="btn btn-secondary btn-success" id ="add_approve_' + data['id'] + '" ng-click="approve(\'add\','+data['id'] +')\">Approve</button>'
          + '<button type="button" class="btn btn-secondary btn-danger" id ="add_deny_' + data['id'] + '" ng-click="deny(\'add\','+data['id'] +')\">Decline</button>'
        + '</div>'
      + '</div>'
    + '</div>'
    + '<div class="row">'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Email:'
      + '</div>'
      + '<div class="col-sm-10" style = "padding: 5px 0">'
        + data['email']
      + '</div>'
    + '</div>'
    + '<div class="row">'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Dataset Name:'
      + '</div>'
      + '<div class="col-sm-10" style = "padding: 5px 0">'
        + data['dataset_name']
      + '</div>'
    + '</div>'
    + '<div class="row">'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Url:'
      + '</div>'
      + '<div class="col-sm-10" style = "padding: 5px 0">'
        + '<a href="'+ data['url'] + '">' +data['url'] +'</a>'
      + '</div>'
    + '</div>'
    + '<div class="row">'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Description:'
      + '</div>'
      + '<div class="col-sm-10" style = "padding: 5px 0">'
        + '<p>' + data['intro'] + '</p>'
      + '</div>'
    + '</div>'
  }
  else if(type == 'edit'){
    res = '<div class="container-fluid" style = "border-bottom-width:2px; border-bottom-color:Grey; border-bottom-style: solid; width:95%">'
     + '<div class="row">'
     + '<div class="col-sm-2" style = "padding: 5px 0">'
     + 'First Name:'
     + '</div>'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
      + data['firstname']
      + '</div>'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Last Name:'
      + '</div>'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        +data['lastname']
      +'</div>'
      + '<div class="col-sm-4" style = "padding: 5px 0">'
      + '<div class="btn-group" style = "float: right;" role="group" aria-label="Basic example">'
          + '<button type="button" class="btn btn-secondary btn-success" id ="edit_approve_' + data['id'] + '" ng-click="approve(\'edit\','+data['id'] +')\">Approve</button>'
          + '<button type="button" class="btn btn-secondary btn-danger" id ="edit_deny_' + data['id'] + '" ng-click="deny(\'edit\','+data['id'] +')\">Decline</button>'
        + '</div>'
      + '</div>'
    + '</div>'
    + '<div class="row">'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Email:'
      + '</div>'
      + '<div class="col-sm-10" style = "padding: 5px 0">'
        + data['email']
      + '</div>'
    + '</div>'
    + '<div class="row">'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Dataset Name:'
      + '</div>'
      + '<div class="col-sm-10" style = "padding: 5px 0">'
        + data['dataset_name']
      + '</div>'
    + '</div>'
  }
  else if(type == 'delete'){
    res = '<div class="container-fluid" style = "border-bottom-width:2px; border-bottom-color:Grey; border-bottom-style: solid; width:95%">'
     + '<div class="row">'
     + '<div class="col-sm-2" style = "padding: 5px 0">'
     + 'First Name:'
     + '</div>'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
      + data['firstname']
      + '</div>'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Last Name:'
      + '</div>'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        +data['lastname']
      +'</div>'
      + '<div class="col-sm-4" style = "padding: 5px 0">'
      + '<div class="btn-group" style = "float: right;" role="group" aria-label="Basic example">'
          + '<button type="button" class="btn btn-secondary btn-success" id ="delete_approve_' + data['id'] + '" ng-click="approve(\'delete\','+data['id'] +')\">Approve</button>'
          + '<button type="button" class="btn btn-secondary btn-danger" id ="delete_deny_' + data['id'] + '" ng-click="deny(\'delete\','+data['id'] +')\">Decline</button>'
        + '</div>'
      + '</div>'
    + '</div>'
    + '<div class="row">'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Email:'
      + '</div>'
      + '<div class="col-sm-10" style = "padding: 5px 0">'
        + data['email']
      + '</div>'
    + '</div>'
    + '<div class="row">'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Dataset Name:'
      + '</div>'
      + '<div class="col-sm-10" style = "padding: 5px 0">'
        + data['dataset_name']
      + '</div>'
    + '</div>'
    + '<div class="row">'
      + '<div class="col-sm-2" style = "padding: 5px 0">'
        + 'Reason:'
      + '</div>'
      + '<div class="col-sm-10" style = "padding: 5px 0">'
        + data['reason']
      + '</div>'
    + '</div>'
  }
  return res;
}

gen_checkbox = function(dataset_name, annotation_list, count){
  var part = '<div class = "row" style="margin: 0 0">' +
                  '<div class = "col-sm-5" style="padding:0 0; vertical-align: middle">' +
                      '<div><input type="checkbox" id = "dataset_check_' + count + '" ng-click="check_dataset('+ count +')" value="'+ dataset_name + '" checked> ' + dataset_name + '</input></div>'+
                  '</div>'+
                  '<div class = "col-sm-5" id = "annotation_check_' + count + '" style="padding:0 0; vertical-align: middle">';
  annotation_list.forEach(function(value){
    part += '<div><input type="checkbox" value="'+ value + '" checked> ' + value + '</input></div>';
  })
  part +=   '</div>'+ '</div>'
  return part;
  // return '<div><input type="checkbox" value="'+ value + '" checked> ' + value + '</input></div>';
}