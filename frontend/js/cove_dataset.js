cove.controller('DatasetCtrl',function ($scope, $http, $window, $compile, $rootScope, $routeParams){
	$scope.$on('$viewContentLoaded', function(event){
        if($routeParams.id){
            id_num = $routeParams.id;
            $http.get(DATASET_URL+'?id='+id_num).then(function(results) {
                console.log(results);
                $scope.id = results.data.id;
                $scope.name = results.data.name;
                $scope.url = results.data.url;
                $scope.thumbnail = results.data.thumbnail;
                $scope.year = results.data.year;
                $scope.creator = results.data.creator;
                $scope.description = results.data.description;
                $scope.size = results.data.size;
                $scope.num_cat = results.data.num_cat;
                $scope.keywords = results.data.keywords;
                $scope.conferences = results.data.conferences;
                $scope.tasks = results.data.tasks;
                $scope.topics = results.data.topics;
                $scope.types = results.data.types;
                $scope.annotations = results.data.annotations;
                $scope.citations = results.data.citations;
                $scope.institutions = results.data.institutions;
                
                
                $scope.thumbnailTrue = 'true';
                $scope.sizeTrue = 'true';        
                $scope.num_catTrue = 'true';            
                $scope.conferencesTrue = 'true';               
                $scope.annotationsTrue = 'true';              
                $scope.citationsTrue = 'true';
                
                if($scope.thumbnail == ''){
                     $scope.thumbnailTrue = 'false';
                }
                if($scope.size == ''){
                     $scope.thumbnailTrue = 'false';
                }
                if($scope.num_cat == ''){
                     $scope.num_catTrue = 'false';
                }
                if($scope.conferences == ''){
                     $scope.conferencesTrue = 'false';
                }
                if($scope.annotations == ''){
                     $scope.annotationsTrue = 'false';
                }
                if($scope.citations == ''){
                     $scope.citationsTrue = 'false';
                }      
            }) 
        }
	});

    $scope.insert_data = function(data){
        $('#dataset_name').text(data['name']);
        var author = $('<b><i>' + data['creator'] +'</i></b>');
        author.appendTo($('#authors'));
        var description = $('<p></p>').text(data['description']);
        description.appendTo($('#description'))
        var tasks = $('<p></p>').text(data['tasks'].join(", "));
        tasks.appendTo($('#tasks'));
        var datatypes = $('<p></p>').text(data['datatypes'].join(", "));
        datatypes.appendTo($('#datatypes'));
        var topics = $('<p></p>').text(data['topics'].join(", "));
        topics.appendTo($('#topics'));
        for(var i = 0; i < data['thumbnails'].length; i++){ 
            $('<img>', {src: data['thumbnails'][i]}).appendTo($('#thumbnails'));
        }
        var source = $('<a></a>').attr({target: "_blank", href: data['url']}).text(data['url']);
        source.appendTo($('#url'));
    };

    $scope.load_page = function(id){
        request_url = REQUEST_DST_URL + "id?dataset_id=" + id;
        $http.get(request_url)
                .success(function(data){
                    if(data.value != null){
                        $scope.insert_data(data.value);
                    };
                })
            .finally(function(){
                $scope.is_loading = false;   
            });
    };
})