cove.controller('BrowseCtrl', function ($scope, $route, $http, $window, $location, $routeParams, $compile, $rootScope, $routeParams) {
    document.onreadystatechange = function () {
      $scope.loaded=false;
      var state = document.readyState
      if (state == 'complete') {
            $scope.loaded=true;
      }
    }
        
    $scope.search_type = "Text";
    $scope.ret_num = 10;
    $scope.browse_list_by_dataset = [];
    // contains display cards, which contains title name and pic urls
    $scope.search_queries = new Array(3); // text, problem, dataset, annotation, category, conference
    $scope.search_queries_dst = new Array(7);
    $scope.browse_list_by_annotation = [];
    $scope.datasample_list = [];
    $scope.global_id = 0; 
    $scope.is_loading = false;
    $scope.is_advance = false;
    $scope.search_datasample = $route.current.$$route.search_datasample;
    $scope.searchTerm = '';
    $scope.minYear = '';
    $scope.maxYear = '';
    $scope.publication = false;
    
    if ($routeParams.search){
        $scope.searchTerm = $routeParams.search;
    }
    if ($routeParams.minyear){
        $scope.minYear = $routeParams.minyear;    
    }
    if ($routeParams.maxyear){
        $scope.maxYear = $routeParams.maxyear;        
    }  
    if ($routeParams.publication){
        $scope.publication = true;    
    }
    
    getallAttributes = function(){
        return ($http.get(HOME_URL).then(function(results) {
            $scope.allTasksList = results.data.tasks;
            $scope.allTopicsList = results.data.topics;
            $scope.allTypesList = results.data.types;
            $scope.allAnnotationsList = results.data.annotations;
        }))
    }

    $scope.initializeObj = function (allElems, selectedElems) {
        attrObj = [];
        for (var i = 0; i < allElems.length; i++){
            if (selectedElems.indexOf(allElems[i]) != -1){
                 attrObj.push({Element: allElems[i], Selected: true})   
            }
            else {
                attrObj.push({Element: allElems[i], Selected: false})         
            }                            
        }
        return attrObj;
    }
            
    $scope.tasks = [];
    $scope.topics = [];
    $scope.types = [];
    
    if ($routeParams.task){
        $scope.tasks = $routeParams.task;
    }
    
    if ($routeParams.topic){
        $scope.topics = $routeParams.topic;
    }
    
    if ($routeParams.type){
        $scope.types = $routeParams.type;
    }
    
    getallAttributes().then(function(results) {
        $scope.allTasks = $scope.initializeObj($scope.allTasksList, $scope.tasks);
        $scope.allTopics = $scope.initializeObj($scope.allTopicsList, $scope.topics);
        $scope.allTypes = $scope.initializeObj($scope.allTypesList, $scope.types);
    })      

    $(document).on('click', '#filter', function(){
            $('#filters').slideToggle();
        }
    )
    
    $(document).on('mouseenter', '.panel', function(){
            var heading = angular.element((event.target).querySelector('.panel-heading'));
            var details = angular.element((event.target).querySelector('.panel-details'));
            heading.slideUp();
            details.slideDown();
        }
    )

    $(document).on('mouseleave', '.panel', function(){
            var heading = angular.element((event.target).querySelector('.panel-heading'));
            var details = angular.element((event.target).querySelector('.panel-details'));
            heading.slideDown();
            details.slideUp();
        }
    )
    $scope.resultsURL = '';
    
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
        
    function replaceUrlParam(url, paramName, paramValue) {
        if (paramValue == null) {
            paramValue = '';
        }
        var pattern = new RegExp('\\b('+paramName+'=).*?(&|$)');
        if (url.search(pattern)>=0) {
            return url.replace(pattern,'$1' + paramValue + '$2');
        }
        url = url.replace(/\?$/,'');
        return url + (url.indexOf('?')>0 ? '&' : '?') + paramName + '=' + paramValue;
    }
   
    var queryParams = $location.url().split('?')[1];
    
    
    var resultsURL = RESULTS_URL + '?' + queryParams;
    
    $http.get(resultsURL).then(function(results) {
        var numTotalResults = results.data.length;
        
        // pagination 
        // page number of last page
        var last = Math.ceil(numTotalResults/TOTAL_DISP);
                
        // last cannot be less than 1
        if (last < 1) {
            last = 1;    
        }
        
        if ($routeParams.pn){
            var pn = parseInt($routeParams.pn);             
        } else {
            var pn = 1;        
        }
        
        if (pn < 1){
            pn = 1;        
        } else if (pn > last) {
            pn = last;
        }
        
        var limStart = (pn - 1) * TOTAL_DISP;
        var limEnd = limStart + TOTAL_DISP;
        
        var datasets = results.data.slice(limStart,limEnd);          
       
        var paginationCtrls = '';
        
        // if more than 1 pg worth of results
        if (last != 1) {
            if (pn > 1){
                var previous = pn - 1;
                newURL = replaceUrlParam('/#'+$location.url(), 'pn', previous);
                paginationCtrls += "<span style='font-size:22px'><a href='" + newURL + "'>&#171;</a></span> &nbsp; &nbsp; ";
			
            // Render clickable number links that should appear on the left of the target page number
    			for( var i = pn-4; i < pn; i++){
    				if (i > 0){
                    newURL = replaceUrlParam('/#'+$location.url(), 'pn', i);
                    paginationCtrls += "<a href=" + newURL + ">" + i + "</a> &nbsp; ";
    				}
    		    }
    	    }
    		// Render the target page number, but without it being a link
    		paginationCtrls += "<span>" + pn + " &nbsp;</span>";
    		// Render clickable number links that should appear on the right of the target page number
    		for(var i = pn+1; i <= last; i++){
                newURL = replaceUrlParam('/#'+$location.url(), 'pn', i);
                paginationCtrls += " <a href=" + newURL + ">" + i + "</a> &nbsp; ";
                if(i >= pn+4){
                    break;
                }
    		}
    		// This does the same as above, only checking if we are on the last page, and then generating the "Next"
    	    if (pn != last) {
                var next = pn + 1;
                newURL = replaceUrlParam('/#'+$location.url(), 'pn', next);
                paginationCtrls += " &nbsp; &nbsp; <span style='font-size:22px'><a href=" + newURL + ">&#187;</a></span> ";
    	    }
    	}
    
    	else {
    		paginationCtrls += "1";
    	}        
                    
        var count = datasets.length; //mysqli_num_rows($result);
        
        var fullRow = Math.floor(count/NUM_COL);
        	
        var rem = count % NUM_COL;
        	
        //var resultArray = mysqli_fetch_all($result,MYSQLI_ASSOC);
        var index = 0;
        	
        var lgSize = 12/NUM_COL;
        var mdSize = 12/(NUM_COL*0.75);
        var smSize = 12/(NUM_COL*0.5);
            
        var disp = ''
    	
    	disp += "<div class='container'>";
    	disp += "<div class='row'>";
    	disp += "<div class='col-xs-12 col-sm-12 col-md-12 col-lg-12'>";
    	
    	for (var i = 0; i < fullRow; i++){
    		disp += "<div class='row'>";
    		for (var j = 0; j < NUM_COL; j++) {
    			disp += "<div class='col-xs-12 col-sm-" + smSize + " col-md-" + mdSize + " col-lg-" + lgSize + "'>";
    			var dataset = datasets[index];
                
                var conferencesList = dataset['conferences'];
                var tasksList = dataset['tasks'];
                var topicsList = dataset['topics'];
                var typesList = dataset['types'];
    			
    			disp += "<a href='#/dataset?id=" + dataset['id'] + "' style='color:inherit;text-decoration:none;cursor:pointer;'>";
    			disp += "<div class='panel'>";
    			disp += "<div class='panel-heading'>";
    			if (dataset['thumbnail'] != ''){
    				disp += "<img style='height: 100%; width: 100%; object-fit: fill' src=" + dataset['thumbnail'] + " altSrc='img/grey-background.jpg' onerror='this.src= $(this).attr(&#039;altSrc&#039;)'>";
    			}
    			else{
    				disp += "<img style='height: 100%; width: 100%; object-fit: fill' src='img/grey-background.jpg'>";
    			}
    			disp += "</div>";				
    			disp += "<div class='panel-body'>";
    			disp += "<div><span id='yr_conf'>" + dataset['year'] + "</span>";
    			if (dataset['conferences'] != ''){
    				disp +=  "<span id='yr_conf'>&nbsp;&nbsp;&#9679;&nbsp;&nbsp;" + conferencesList + "</span></div>";				
    			}
    			else {
    				disp += "</div>";
    			}		
    			disp += "<div><span id='name'>"+ dataset['name'] + "</span></div>";
    			disp += "</div>";
    			
    			disp += "<div class='panel-details'>";
    			disp += "<div id='metalabel'>Tasks:</div>";
    			disp += "<div id='metainfo'>" + tasksList + "</div>";
    			disp += "<div id='metalabel'>Topics:</div>";
    			disp += "<div id='metainfo'>" + topicsList + "</div>";
    			disp += "<div id='metalabel'>Data Types:</div>";
    			disp += "<div id='metainfo'>" + typesList + "</div>";
    			disp += "</div>";
    			
    			
    			disp += "<div class='panel-footer'>";
    			disp += "<span id='link'><a href=" + dataset['url'] + " target='_blank'><i class='fas fa-link'></i></a></span>";
    			disp += "</div>";
    										
    			disp += "</div>";
    			disp += "</div>";
    			disp += "</a>";
    			index += 1;
    		}
    		disp += "</div>";
    	}
    	if (rem > 0){
    		var blankCol = NUM_COL - rem;
    		disp += "<div class='row'>";
    		for (var j = 0; j < rem; j++){
    			disp += "<div class='col-xs-12 col-sm-" + smSize + " col-md-" + mdSize + " col-lg-" + lgSize + "'>";
    			var dataset = datasets[index];
    				
                var conferencesList = dataset['conferences'];
                var tasksList = dataset['tasks'];
                var topicsList = dataset['topics'];
                var typesList = dataset['types'];
    			
    			disp += "<a href='#/dataset?id=" + dataset['id'] + "' style='color:inherit;text-decoration:none;cursor:pointer;'>";
    			disp += "<div class='panel'>";
    			disp += "<div class='panel-heading'>";
    			if (dataset['thumbnail'] != ''){
    				disp += "<img style='height: 100%; width: 100%; object-fit: fill' src=" + dataset['thumbnail'] + " altSrc='img/grey-background.jpg' onerror='this.src= $(this).attr(&#039;altSrc&#039;)'>";
    			}
    			else{
    				disp += "<img style='height: 100%; width: 100%; object-fit: fill' src='img/grey-background.jpg'>";
    			}
    			disp += "</div>";				
    			disp += "<div class='panel-body'>";
    			disp += "<div><span id='yr_conf'>" + dataset['year'] + "</span>";
    			if (dataset['conferences'] != ''){
    				disp +=  "<span id='yr_conf'>&nbsp;&nbsp;&#9679;&nbsp;&nbsp;" + conferencesList + "</span></div>";				
    			}
    			else {
    				disp += "</div>";
    			}		
    			disp += "<div><span id='name'>"+ dataset['name'] + "</span></div>";
    			disp += "</div>";
    			
    			disp += "<div class='panel-details'>";
    			disp += "<div id='metalabel'>Tasks:</div>";
    			disp += "<div id='metainfo'>" + tasksList + "</div>";
    			disp += "<div id='metalabel'>Topics:</div>";
    			disp += "<div id='metainfo'>" + topicsList + "</div>";
    			disp += "<div id='metalabel'>Data Types:</div>";
    			disp += "<div id='metainfo'>" + typesList + "</div>";
    			disp += "</div>";
    			
    			
    			disp += "<div class='panel-footer'>";
    			disp += "<span id='link'><a href=" + dataset['url'] + " target='_blank'><i class='fas fa-link'></i></a></span>";
    			disp += "</div>";
    										
    			disp += "</div>";
    			disp += "</div>";
    			disp += "</a>";
    			index += 1;
    		}
    		disp += "</div>";		
    	}
    	disp += "</div>";
    	disp += "</div>";
    	disp += "</div>";
        
      angular.element(document.getElementById('dataset-display')).append($compile(disp)($scope))
      //(disp).appendTo("#dataset-display");
        $(paginationCtrls).appendTo("#pagination");
    });



    $scope.$on('$viewContentLoaded', function(event){
        if($routeParams.query_type){
            if($routeParams.query_type === "text"){
                $scope.search_type = "Text";
                $scope.search_text = $routeParams.query;
            }
            else if($routeParams.query_type === "problem"){
                $scope.search_type = "Problem";
                $scope.search_text = $routeParams.problem;
            }
            else if($routeParams.query_type === "dataset"){
                $scope.search_type = "Dataset";
                $scope.search_text = $routeParams.dataset;
            }
            else if($routeParams.query_type === "annotation"){
                $scope.search_type = "Annotation";
                $scope.search_text = $routeParams.annotation;
            }
            else if($routeParams.query_type === "category"){
                $scope.search_type = "Category";
                $scope.search_text = $routeParams.category;
            }
            else if($routeParams.query_type === "name"){
                $scope.search_type = "Name";
                $scope.search_text = $routeParams.name;
            }
            else if($routeParams.query_type === "institution"){
                $scope.search_type = "Institution";
                $scope.search_text = $routeParams.institution;
            }
            else if($routeParams.query_type === "conference"){
                $scope.search_type = "Conference";
                $scope.search_text = $routeParams.conference;
            }
            else if($routeParams.query_type === "advanced"){
                $scope.is_advance = true;
                if($scope.search_datasample){
                    $scope.search_queries[0] = $routeParams.dataset;
                    $scope.search_queries[1] = $routeParams.category;
                    $scope.search_queries[2] = $routeParams.annotation;
                }
                else{
                    $scope.search_queries_dst[0] = $routeParams.task;
                    $scope.search_queries_dst[1] = $routeParams.year;
                    $scope.search_queries_dst[2] = $routeParams.insti;
                    $scope.search_queries_dst[3] = $routeParams.conf;
                    $scope.search_queries_dst[4] = $routeParams.dtype;
                    $scope.search_queries_dst[5] = $routeParams.atype;
                    $scope.search_queries_dst[6] = $routeParams.topic;
                }
            }
            else{
                console.log("undefined behavior");
            }
            $scope.ret_num = $routeParams.num;
            if($scope.search_datasample){
                $('#search_dataset_option').css("display" , "none");
                $('#search_datasample_option').css("display" , "");
                $('#search_target').text("Datasample(" + $scope.ret_num + ")");
            }
            else{
                $('#search_target').text("Dataset");
                $('#search_dataset_option').css("display" , "");
                $('#search_datasample_option').css("display" , "none");

            }
            if(!$scope.is_advance){
                $("#type_button").text($scope.search_type);
            }
            $scope.search(0);
        }
    });

    $scope.set_type = function(type){
        $("#type_button").text(type);
        $scope.search_type = type;
    };

    $scope.set_num = function(num){
        $('#search_target').text("Datasample(" + num + ")");
        $scope.ret_num = num;
        if(!$scope.search_datasample){
            $scope.search_type = 'Text';
            $("#type_button").text("Search by");
        }
        $scope.search_datasample = true;
        if($scope.is_advance){
            $("#advanced_hide_dst").css("display" , "none");
            $("#advanced_hide").fadeIn(600);
        }
        $('#search_dataset_option').css("display" , "none");
        $('#search_datasample_option').css("display" , "");
    };

    $scope.search_dataset = function(){
        $('#search_target').text("Dataset");
        if($scope.is_advance){
            $("#advanced_hide").css("display" , "none");
            $("#advanced_hide_dst").fadeIn(600);
        }
        if($scope.search_datasample){
            $scope.search_type = 'Name';
            $("#type_button").text("Search by");
        }
        $scope.search_datasample = false;
        $('#search_dataset_option').css("display" , "");
        $('#search_datasample_option').css("display" , "none");
    }

    $scope.go_to_download = function(){
        $window.open("#/download", "_self");
        // var new_tab = $window.open("/#/download", '_blank');
        // new_tab.download_list = $rootScope.download_list;
    };
    $scope.advance_span = function(){
        if($("#dd_icon").hasClass("octicon-chevron-down")){
            $scope.is_advance = true;
            $("#type_button").text("Search by");
            if($scope.search_datasample){
                $("#advanced_hide").fadeIn(600);
            }
            else{
                $("#advanced_hide_dst").fadeIn(600);
            }
            $("#dd_icon").removeClass("octicon-chevron-down");
            $("#dd_icon").addClass("octicon-chevron-up");
            $(".jumbotron").css("padding-bottom", "1.5rem");
        }
        else{
            $scope.is_advance = false;
            if($scope.search_datasample){
                $("#advanced_hide").fadeOut(400);
            }
            else{
                $("#advanced_hide_dst").fadeOut(400);
            }
            $("#dd_icon").addClass("octicon-chevron-down");
            $("#dd_icon").removeClass("octicon-chevron-up");
            $(".jumbotron").css("padding-bottom", "1.5rem");
        }
    };

    $scope.insert_title = function(){
        var reminder = "Below are result " + ($scope.search_datasample ? "datasamples" : "datasets") + " for your query: ";
        if($scope.is_advance){
            if($scope.search_datasample){
                if($scope.search_queries[0]){
                    reminder += "dataset = " + $scope.search_queries[0] + ", ";
                }
                if($scope.search_queries[1]){
                    reminder += "category = " + $scope.search_queries[1] + ", ";
                }
                if($scope.search_queries[2]){
                    reminder += "annotation = " + $scope.search_queries[2] + ", ";
                }
            }
            else{
                if($scope.search_queries_dst[0]){
                    reminder += "task = " + $scope.search_queries_dst[0] + ", ";
                }
                if($scope.search_queries_dst[1]){
                    reminder += "year = " + $scope.search_queries_dst[1] + ", ";
                }
                if($scope.search_queries_dst[2]){
                    reminder += "institution = " + $scope.search_queries_dst[2] + ", ";
                }
                if($scope.search_queries_dst[3]){
                    reminder += "conference = " + $scope.search_queries_dst[3] + ", ";
                }
                if($scope.search_queries_dst[4]){
                    reminder += "data_type = " + $scope.search_queries_dst[4] + ", ";
                }
                if($scope.search_queries_dst[5]){
                    reminder += "annotation = " + $scope.search_queries_dst[5] + ", ";
                }
                if($scope.search_queries_dst[6]){
                    reminder += "topic = " + $scope.search_queries_dst[6] + ", ";
                }
            }
        }
        else{
            reminder += $scope.search_type + " = " + $scope.ge + ($scope.search_datasample ? "," : ".");
        }
        if($scope.search_datasample){
            reminder += " you can group them by: ";
        }
        else{
            reminder += " Click to view introduciton."
        }
        var title = $('<div/>',{
                    id: "title_message",
                    css: {
                        "background-color": "rgb(235, 230, 228)",
                        "font-size": "28px",
                        "padding-bottom": "0.5rem",
                        "margin-bottom": "2px",
                    },
                    text: reminder,
                });
        if($scope.search_datasample){
            var button = $(gen_group_button());
            title.append(button);
        }
        title.insertBefore($('#browse-side'));        
        $compile($('#title_message'))($scope);
    }

    $scope.group_by_dataset = function(){
        $("#group_button").text("dataset");
        $rootScope.browse_list = [];
        if($scope.browse_list_by_dataset.length === 0){
            for(var i=0; i<$scope.datasample_list.length; ++i){
                var sample = $scope.datasample_list[i];
                var find = 0;
                for(var j=0; j<$scope.browse_list_by_dataset.length; ++j){
                    if(sample.dataset_name == $scope.browse_list_by_dataset[j].display_name){
                        find = 1;
                        $scope.browse_list_by_dataset[j].sample_list.push(sample);
                    }
                }
                if(find === 0){
                    var temp = new displaycard(sample.dataset_name, $scope.global_id);
                    temp.sample_list.push(sample);
                    $rootScope.browse_list.push(temp);
                    $scope.browse_list_by_dataset.push(temp);
                    ++$scope.global_id;
                }
            }
        }
        else{
            for(var i=0; i < $scope.browse_list_by_dataset.length; i++){
                $rootScope.browse_list.push($scope.browse_list_by_dataset[i]);
            }
        }
        $rootScope.construct_browse_disp(false);
    };

    $scope.group_by_annotation = function(){
        $("#group_button").text("annotation");
        $rootScope.browse_list = [];
        if($scope.browse_list_by_annotation.length === 0){
            for(var i=0; i<$scope.datasample_list.length; ++i){
                var sample = $scope.datasample_list[i];
                var find = 0;
                for(var j=0; j<$scope.browse_list_by_annotation.length; ++j){
                    if(sample.annotation == $scope.browse_list_by_annotation[j].display_name){
                        find = 1;
                        $scope.browse_list_by_annotation[j].sample_list.push(sample);
                    }
                }
                if(find === 0){
                    var temp = new displaycard(sample.annotation, $scope.global_id);
                    temp.sample_list.push(sample);
                    $rootScope.browse_list.push(temp);
                    $scope.browse_list_by_annotation.push(temp);
                    ++$scope.global_id;
                }
            }
        }
        else{
            for(var i=0; i < $scope.browse_list_by_annotation.length; i++){
                $rootScope.browse_list.push($scope.browse_list_by_annotation[i]);
            }
        }
        $rootScope.construct_browse_disp(false);
    };

    $scope.group_by_dontgroup = function(){
        $("#group_button").text("dont\' group");
        $('#browse-side').empty();
        var browse_list = [];
        for(var i=0; i<$scope.datasample_list.length; ++i){
            browse_list.push($scope.datasample_list[i].pic_url);
        }
        var barrels = new Barrels($('#browse-side'), browse_list, 180);
    };

    $scope.click_search_button = function(){
        if($scope.is_advance){
            if($scope.search_datasample){                
                $scope.search_queries[0] = $("#adv-dataset").val();            
                $scope.search_queries[1] = $("#adv-cat").val();
                $scope.search_queries[2] = $("#adv-annote").val();
            }
            else{
                $scope.search_queries_dst[0] = $("#adv-task").val();
                $scope.search_queries_dst[1] = $("#adv-year").val();
                $scope.search_queries_dst[2] = $("#adv-insti").val();
                $scope.search_queries_dst[3] = $("#adv-confer").val();
                $scope.search_queries_dst[4] = $("#adv-dtype").val();
                $scope.search_queries_dst[5] = $("#adv-atype").val();
                $scope.search_queries_dst[6] = $("#adv-topic").val();
            }
        }
        else{
            $scope.search_text = $("#search-text").val();
        }
        $scope.search(1);
    }

    $scope.search = function(flag){ //flag to infer whether to replace state or not
        $scope.datasample_list = [];
        $scope.browse_list_by_annotation = [];
        $scope.browse_list_by_dataset = [];
        var request_url = "";
        var target_url = window.location.protocol + "//" + window.location.host;
        if($scope.is_advance){
            if($scope.search_datasample){
                request_url = REQUEST_URL + 'advanced?dataset=' + $scope.search_queries[0] + 
                '&category=' + $scope.search_queries[1] +'&annotation='+ $scope.search_queries[2] + 
                '&num=' + $scope.ret_num.toString();
                target_url += "/#/search/" + 'advanced?dataset=' + $scope.search_queries[0] + 
                '&category=' + $scope.search_queries[1] +'&annotation='+ $scope.search_queries[2] + 
                '&num=' + $scope.ret_num.toString();
            }
            else{
                request_url = REQUEST_DST_URL + 'advanced?task=' + $scope.search_queries_dst[0] + 
                '&year=' + $scope.search_queries_dst[1] +'&insti='+ $scope.search_queries_dst[2] + 
                '&conf='+ $scope.search_queries_dst[3] + '&dtype='+ $scope.search_queries_dst[4] +
                '&atype='+ $scope.search_queries_dst[5] + '&topic='+ $scope.search_queries_dst[6] +
                '&num=' + $scope.ret_num.toString();
                target_url = "/#/search_dataset/" + 'advanced?task=' + $scope.search_queries_dst[0] + 
                '&year=' + $scope.search_queries_dst[1] +'&insti='+ $scope.search_queries_dst[2] + 
                '&conf='+ $scope.search_queries_dst[3] + '&dtype='+ $scope.search_queries_dst[4] +
                '&atype='+ $scope.search_queries_dst[5] + '&topic='+ $scope.search_queries_dst[6] +
                '&num=' + $scope.ret_num.toString();
            }
        }
        else if($scope.search_type === "Text"){ 
            request_url = REQUEST_URL + 'text?query='+ $scope.search_text + '&num=' + $scope.ret_num.toString();
            target_url += "/#/search/" + 'text?query='+ $scope.search_text + '&num=' + $scope.ret_num.toString();
        }
        else if($scope.search_type === "Problem"){
            $window.alert('This function hasn\'t implemented yet.');
        }
        else if($scope.search_type === "Dataset"){
            request_url = REQUEST_URL + 'dataset?dataset=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
            target_url += "/#/search/" + 'dataset?dataset=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
        }
        else if($scope.search_type === "Category"){
            request_url = REQUEST_URL + 'category?category=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
            target_url += "/#/search/" + 'category?category=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
        }
        else if($scope.search_type === "Annotation"){
            if($scope.search_datasample){
                request_url = REQUEST_URL + 'annotation?annotation=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
                target_url += "/#/search/" + 'annotation?annotation=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
            }
            else{
                request_url = REQUEST_DST_URL + 'annotation?annotation=' + $scope.search_text + '&num=10';
                target_url += "/#/search_dataset/" + 'annotation?annotation=' + $scope.search_text + '&num=10';
            }
        }
        else if($scope.search_type === "Name"){
            request_url = REQUEST_DST_URL + 'name?name=' + $scope.search_text + '&num=10';
            target_url += "/#/search_dataset/" + 'name?name=' + $scope.search_text + '&num=10';
        }
        else if($scope.search_type === "Conference"){
            request_url = REQUEST_DST_URL + 'conference?conference=' + $scope.search_text + '&num=10';
            target_url += "/#/search_dataset/" + 'conference?conference=' + $scope.search_text + '&num=10';
        }
        else if($scope.search_type === "Year"){
            request_url = REQUEST_DST_URL + 'year?year=' + $scope.search_text + '&num=10';
            target_url += "/#/search_dataset/" + 'year?year=' + $scope.search_text + '&num=10';
        }
        else if($scope.search_type === "Data_type"){
            request_url = REQUEST_DST_URL + 'dtype?dtype=' + $scope.search_text + '&num=10';
            target_url += "/#/search_dataset/" + 'dtype?dtype=' + $scope.search_text + '&num=10';
        }
        else if($scope.search_type === "Institution"){
            request_url = REQUEST_DST_URL + 'institution?institution=' + $scope.search_text + '&num=10';
            target_url += "/#/search_dataset/" + 'institution?institution=' + $scope.search_text + '&num=10';
        }
        else{
            console.log("undefined behavior");
        }
        console.log(request_url);
        console.log(target_url);
        if(flag === 1){
            history.replaceState({}, "a", target_url);
        }
        if(request_url !== ""){
            $('#browse-side-thumb').empty();
            $scope.is_loading = true;
            $http.get(request_url)
                .success(function(data){
                    if(data.value != null){
                        $scope.datasample_list = [];
                        var value = data.value;
                        for(var i=0; i<value.length; ++i){
                            var dataset_name = value[i].name;
                            var dataset_url = window.location.protocol + "//" + window.location.host + "/#/dataset/" + value[i].id;
                            var temp_card = new displaycard(dataset_name, $scope.global_id, false, dataset_url);
                            for(var j=0; j<value[i].datasample_preview.length; ++j){
                                var sample = value[i].datasample_preview[j];
                                for(var k=0; k<sample.annotation.length; ++k){
                                    var temp = new datasample(dataset_name, sample.type, sample.id, sample.path, sample.annotation[k]);
                                    temp_card.sample_list.push(temp);
                                    $scope.datasample_list.push(temp);
                                }
                            }
                            $scope.browse_list_by_dataset.push(temp_card);
                            ++$scope.global_id;
                        }
                        $("#title_message").remove();
                        $scope.insert_title();
                        $scope.group_by_dataset();
                    };
                })
            .finally(function(){
                $scope.is_loading = false;   
            });
        }
    };
});