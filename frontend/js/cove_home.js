cove.controller('HomeCtrl', function ($scope, $route, $http, $location, $window, $compile, $rootScope, $routeParams) {
    $(document).ready(function(){		
        $('#logout_button').hide();
        $('#login_button').show();
    	$('#filter').click(function() {
    		$('#filters').slideToggle('slow');
    	});
    });
        
    $http.get(HOME_URL).then(function(results) {
        $scope.tasks = results.data.tasks;
        $scope.topics = results.data.topics;
        $scope.types = results.data.types;
    })

    $scope.resultsURL = '';
    
    $scope.show_dataset_submit = function(){
        $('#dst_submit').modal('show');
        $("#email-address").val('');
        $("#first-name").val('');
        $("#last-name").val('');
        $("#dst-name").val('');
        $("#dst-url").val('');
        $("#intro").val('');
        $("#send_submission_request").attr("disabled", false);
        $("#messagegoeshere").empty();
        return false;
    };

    $scope.searchSubmit = function() {
        var tasksUrl = '';
        var topicsUrl = '';
        var typesUrl = '';
        var pubUrl = '';
        var minyrUrl = '';
        var maxyrUrl = '';
        var searchUrl = '';            
            
    		var tasks = [];
    		var topics = [];
    		var types = [];
    		var publication = null;
    		
    		var $checkbox = $('input:checkbox');
    		$checkbox.each(function(){
    			if (this.checked){
    				var name = this.name;
    			}
    			switch(name){
    				case 'dataset_task[]':
                    tasksUrl += '&task='+this.id.replace('task_','');

    					//tasks.push(this.id.replace('task_',''));
    					break;
    				case 'dataset_topic[]':
                    topicsUrl += '&topic='+this.id.replace('topic_','');                    
    					//topics.push(this.id.replace('topic_',''));
    					break;
    				case 'dataset_datatype[]':
                    typesUrl += '&type='+this.id.replace('type_','');                    
    					//types.push(this.id.replace('type_',''));
    					break;
    				case 'publication':
                    pubUrl += '&publication=true';
    					//publication = (this.id);
    					break;
    			}
    		});

        if (document.getElementById('minyear').value != ''){
            minyrUrl += '&minyear=' + document.getElementById('minyear').value;
        }
        if (document.getElementById('maxyear').value != ''){
            maxyrUrl += '&maxyear=' + document.getElementById('maxyear').value;
        }
        if (document.getElementById('search').value != ''){
            searchUrl += '&search=' + document.getElementById('search').value;
        }
            $scope.resultsURL = '?pn=1';
            $scope.resultsURL += tasksUrl;
            $scope.resultsURL += topicsUrl;           
            $scope.resultsURL += typesUrl;  
            $scope.resultsURL += pubUrl;  
            $scope.resultsURL += minyrUrl;  
            $scope.resultsURL += maxyrUrl;  
            $scope.resultsURL += searchUrl;                    
        }                
          
});