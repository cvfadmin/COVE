from flask import Flask, render_template
#print("content-type:text/html\r\n")

render_template('templates/header.html')


# print("""
# <html lang="en"> 
# 	<body>""")

# import 'templates/header.py'
# print ("""
# 	</body>
# </html>""")

# 	# print("""
# 	# 	<h1>Hello</h1> """)

# 	# 	i = 1 

# 	# 	while i < 10:
# 	# 		print("<p>" + str(i) + "</p>")
# 	# 		i += 1




# <?php $query_base = "FROM datasets"; ?>

# <!doctype html>
# <html lang="en">
	
#   <head>

#     <meta charset="utf-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

#    	<?php include('config/setup.php'); ?>
   	
#    	<title><?php echo $site_title;?></title>

#   </head>
  
#   <body>
    
#     <?php include('template/header.php'); ?>    
	
#     <!-- SHOWCASE -->
#     <section id="showcase">
#     	<div class="container">
#     		<div class="row center-xs center-sm center-md center-lg middle-xs middle-sm middle-md middle-lg">
#     			<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
#     				<h1><img id="left-logo" src="img/nsf.png"></img></span>Welcome to <span class="primary-text">COVE</span><img id="right-logo" src="img/cvf.png"></h1>
#     				<p>COVE is an online repository for computer vision datasets and tools. It is intended to aid the computer vision research community and serve as a centralized reference for all datasets in the field. If you are a researcher with a dataset not currently in COVE, please help make this site as comprehensive a resource as possible for the community and add it to the database!</p> 
#     			</div>
#     		</div>
#     	</div>
#     </section>
    
#     <!-- CONTROLS -->
# 	<section id="controls">
# 		<div class="container">
# 			<div class="row start-xs start-sm start-md start-lg">
# 				<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
# 					<h2>Datasets</h2>
# 				</div>
# 				<div class="container">
# 					<div class="row start-xs start-sm start-md start-lg">
# 						<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
# 							<nav id="filternav">
# 								<ul>
# 									<li id="filter"><img src="https://png.icons8.com/windows/40/170B3B/sorting-options.png">Filter</li>
# 									<li id="searchbar"><img src="https://png.icons8.com/metro/40/170B3B/search.png"><span id='search_label'>Search</span><form class='form-inline' id='search_bar'><input type='text' name='search' id='search' placeholder="name, author, keyword"><button id='submit'>Go</button></form></li>
# <!--
# 									<li id="sort"><img src="https://png.icons8.com/ios/40/170B3B/sort-filled.png">Sort</li>
# 									<li id="results">#</li>-->
# 									<li id="add"><img src="https://png.icons8.com/metro/50/170B3B/plus.png">Add Dataset</li></li>

# 								</ul>
# 							</nav>	
# 						</div>						
# 					</div>
# 				</div>
# 			<div>
# 		</div>
# 	</section>
	
# 	<!-- FILTERS -->
# 	<section id="filters">
# 		<div class="container">
# 			<div class="row start-xs start-sm start-md start-lg">			
# 				<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3">
# 					<div class="container">
# 						<div class="row start-xs start-sm start-md start-lg" id="year">
# 							<label>Year</label>
# 						</div>
# 						<div class="row start-xs start-sm start-md start-lg" id="yearrange">
# 							<div class="range">
# 								<input placeholder="Min" type="number" name="minyear" id='minyear' inputmode="numeric" pattern="[0-9]*">
# 								<span style="color:#c9c9c9">-</span>
# 								<input placeholder="Max" type="number" name="maxyear" id='maxyear' inputmode="numeric" pattern="[0-9]*">
# 							</div>								
# 						</div>
						
# 						<div class="row start-xs start-sm start-md start-lg">
# 							<label for='publication' class="checkcontainer">Has Publication<input type="checkbox" id='publication' name='publication'><span class="checkmark"></span></label>
# 						</div>
# 					</div>
# 				</div>
				
# 				<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3">
# 					<label>Tasks</label>
# 					<?php generateCheckbox('tasks','task'); ?>
					
# 				</div>
				
# 				<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3">
# 					<label>Topics</label>
# 					<?php generateCheckbox('topics','topic'); ?>
# 				</div>
				
# 				<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3">
# 					<label>Data Types</label>
# 					<?php generateCheckbox('types','type'); ?>
# 				</div>
# 			</div>
# 		</div>		
# 	</section>


#     <!-- DATASETS -->
#     <section id='datasets'>
#     	<?php generateDisplay(ROW,COL,$query_base); ?>
# 	</section>
    
#     <!-- FOOTER -->
#     <?php include('template/footer.php'); ?>
    	
#   </body>
  
# </html>
