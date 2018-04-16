cove.controller('Dataset_intro',function ($scope, $http, $window, $compile, $rootScope, $routeParams){
	$scope.$on('$viewContentLoaded', function(event){
        if($routeParams.dataset_id){
            $scope.load_page($routeParams.dataset_id);
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