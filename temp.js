		
//		vfVersamento = false;
		
		hasAll			= (document.all != null);
		hasFrames		= (document.frames != null);
		hasGetElement	= (document.getElementById != null);
		
		
		// effettuo un resize dei frame al click del menu hamburger		
        var doCommandResizeByHamburger = function(statusHamburger) {
            parent.doResizeHeader(statusHamburger);
       }
		
		function	ResizeWindow(width, height, marginDeltaX, marginDeltaY, delay) {
			ingrandimento	= 10;
			modified		= false;
			if (document.all) { // Internet Explorer
			   windowWidth	= document.body.clientWidth + marginDeltaX;
			   windowHeight	= document.body.clientHeight + marginDeltaY;
			} else {	// Netscape Navigator oppure altro...
			   windowWidth	= window.outerWidth;
			   windowHeight	= window.outerHeight;
			}
//			alert("Window Width: " + windowWidth + " - WindowHeight: " + windowHeight);
			// Se la finestra non ha le dimensioni specificate, la ingrandisco un pochino e continuo l'animazione
			if (windowWidth != width) {
				// La finestra deve essere ingrandita in larghezza?
				vfEnlargeX = (windowWidth < width);
				if (vfEnlargeX) {
					windowWidth += ingrandimento;
					if ( (windowWidth > width) || (Math.abs(windowWidth - width) < ingrandimento) ) {
						windowWidth = width;
					}
				} else {
					windowWidth -= ingrandimento;
					if ( (windowWidth < width) || (Math.abs(windowWidth - width) < ingrandimento) ) {
						windowWidth = width;
					}
				}
				modified = true;
			}
		
			if (windowHeight != height) {
				// La finestra deve essere ingrandita in altezza?
				vfEnlargeY = (windowHeight < height);
				if (vfEnlargeY) {
					windowHeight += ingrandimento;
					if ( (windowHeight > height) || (Math.abs(windowHeight - height) < ingrandimento) ) {
						windowHeight = height;
					}
				} else {
					windowHeight -= ingrandimento;
					if ( (windowHeight < height) || (Math.abs(windowHeight - height) < ingrandimento) ){
						windowHeight = height;
					}
				}
				modified = true;
			}
			// Se la finestra e' stata ridimensionata allora continuo l'animazione
			if (modified) {
				window.resizeTo(windowWidth, windowHeight);
				setTimeout('ResizeWindow(' + width + ', ' + height + ', ' + marginDeltaX + ", " + marginDeltaY + ", " + delay + ');', delay);
			}			
			
		}
		
		function vaisito(par){
			var win = window.opener;
			if (par == "banche" || par == "home"){
				if (confirm('La presente sessione verra\' terminata. Continuare?')){
					if (par == "banche")
						document.location = "http://www.visura.it" + "/fsBancheDati.asp";
					else if (par == "home")
						document.location = "http://www.visura.it" 
					else if (par == "conto")
						document.location = "http://www.visura.it" + "/fsVersamento.asp";
					if (hasAll) {
						window.document.forms['formgestione'].elements['funzione'].value = "chiudi";
						window.document.forms['formgestione'].submit();								
					}
				}		
			}
			else if (par == "chiudi" ){	
				
					if(win != null){
						win.location =  "https://portaleingmonza.visura.it/homepageAreeTematicheAction.do";		
					}else{
						top.window.location =  "https://portaleingmonza.visura.it/homepageAreeTematicheAction.do";		
					}	
				
				if (hasAll) {
					document.frames.mainFrameVISURA.document.forms['formgestione'].elements['funzione'].value = "chiudi";
					document.frames.mainFrameVISURA.window.document.forms['formgestione'].submit();	
				} else if (hasGetElement) {
					
					mainFrameVISURA.document.forms['formgestione'].elements['funzione'].value = "chiudi";
					mainFrameVISURA.document.forms['formgestione'].submit();	
					/*document.frames.mainFrameVISURA.document.forms['formgestione'].elements['funzione'].value = "chiudi";
					document.frames.mainFrameVISURA.window.document.forms['formgestione'].submit();*/
				}
			} else if (par == "conto") {			
				// Se uso Microsoft Internet Explorer, ricavo la differenza tra l'area client e l'area esterna della finestra
				if (document.all) {
					oldWidth = document.body.clientWidth;
					oldHeight = document.body.clientHeight;
					window.resizeTo(200, 100);
					deltaX = (200 - document.body.clientWidth);
					deltaY = (100 - document.body.clientHeight);
					window.resizeTo(oldWidth + deltaX, oldHeight + deltaY);
				} else {
					deltaX = 0;
					deltaY = 0;
				}
//				if (!vfVersamento) {
					// Allargo la finestra alla velocita' di 100 FPS
					ResizeWindow(540, 600, deltaX, deltaY, 10);
//					alert("https://portaleingmonza.visura.it/versamentoSceltaTipologiaConto.do");
					if (hasAll) {
						setTimeout('document.frames.mainFrameVISURA.frames.content.location.replace("https://portaleingmonza.visura.it/versamentoSceltaTipologiaConto.do?layout=nomenu");', 1500);
					} else if (hasGetElement) {
						setTimeout('mainFrameVISURA.content.location.replace("https://portaleingmonza.visura.it/versamentoSceltaTipologiaConto.do?layout=nomenu");', 1500);
//						alert(mainFrameVISURA.content.location);
					}
/*										
				} else {
					ResizeWindow(400, 160, deltaX, deltaY, 10);
					if (hasAll) {
						document.frames.mainFrameVISURA.location = "barraNavigazione_main.jsp";
					} else if (hasGetElement) {
						mainFrameVISURA.location = "barraNavigazione_main.jsp";
					}
				}
				vfVersamento = !vfVersamento;
*/
			}
		}
		
		function	chiudi() {
			// Se uso Microsoft Internet Explorer, ricavo la differenza tra l'area client e l'area esterna della finestra
			if (document.all) {
				oldWidth = document.body.clientWidth;
				oldHeight = document.body.clientHeight;
				window.resizeTo(200, 100);
				deltaX = (200 - document.body.clientWidth);
				deltaY = (100 - document.body.clientHeight);
				window.resizeTo(oldWidth + deltaX, oldHeight + deltaY);
			} else {
				deltaX = 0;
				deltaY = 0;
			}
		
			ResizeWindow(540, 200, deltaX, deltaY, 10);
			if (hasAll) {
				document.frames.mainFrameVISURA.location = "barraNavigazione_main.jsp";
			} else if (hasGetElement) {
				mainFrameVISURA.location = "barraNavigazione_main.jsp";
			}
		}
		
		function	writeSize() {
			if (document.all) {
				oldWidth = document.body.clientWidth;
				oldHeight = document.body.clientHeight;
				window.resizeTo(200, 100);
				deltaX = (200 - document.body.clientWidth);
				deltaY = (100 - document.body.clientHeight);
				window.resizeTo(oldWidth + deltaX, oldHeight + deltaY);
			} else {
				deltaX = 0;
				deltaY = 0;
			}
			// Ricavo le dimensioni attuali della finestra
			if (document.layers) {	// Netscape Navigator
			   windowWidth	= window.outerWidth;
			   windowHeight	= window.outerHeight;
			} else if (document.all) { // Internet Explorer
			   windowWidth	= document.body.clientWidth + deltaX;
			   windowHeight	= document.body.clientHeight + deltaY;
			}
			alert("Dimensioni attuali della finestra: W:" + windowWidth + " - H:" + windowHeight);
		}
		
		function	showDetails(tipoConto) {
			// Se uso Microsoft Internet Explorer, ricavo la differenza tra l'area client e l'area esterna della finestra
			if (document.all) {
				oldWidth = document.body.clientWidth;
				oldHeight = document.body.clientHeight;
				window.resizeTo(200, 100);
				deltaX = (200 - document.body.clientWidth);
				deltaY = (100 - document.body.clientHeight);
				window.resizeTo(oldWidth + deltaX, oldHeight + deltaY);
			} else {
				deltaX = 0;
				deltaY = 0;
			}
//			if (!vfVersamento) {
				// Allargo la finestra alla velocita' di 100 FPS
				ResizeWindow(750, 500, deltaX, deltaY, 10);
				if (hasAll) {
					setTimeout('document.frames.mainFrameVISURA.frames.content.location.replace("/ECMBKE/InfoConsumiSessione?filter=' + tipoConto + '");', 0);
				} else if (hasGetElement) {
					setTimeout('mainFrameVISURA.content.location.replace("/ECMBKE/InfoConsumiSessione?filter=' + tipoConto + '");', 0);
				}
/*				
			} else {
				ResizeWindow(400, 160, deltaX, deltaY, 10);
				if (hasAll) {
					document.frames.mainFrameVISURA.location = "barraNavigazione_main.jsp";
				} else if (hasGetElement) {
					mainFrameVISURA.location = "barraNavigazione_main.jsp";
				}
			}			
			vfVersamento = !vfVersamento;
*/			
		}
		
	