<!doctype html>
<html lang="en">
  <head>
    % include('head.tpl', title='Head')
  </head>
  <body>
  % include('top_nav.tpl', title='Top navigation')

<div class="container-fluid">
  <div class="row">
    
	% include('nav.tpl', title='Navigation')

    <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-md-4">
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">

    <form action="/load_data" method="GET">
    <div class="form-group">
    <div class="alert alert-primary" role="alert">
      <span>{{developer_name}}</span>
      <span>{{developer_organization}}</span>
    </div>
    <div class="tenor-gif-embed" data-postid="13186419" data-share-method="host" data-width="400px" data-aspect-ratio="1.21760391198044">
    </div><script type="text/javascript" async src="https://tenor.com/embed.js"></script>
    <br>
    <span style="margin:15px 0">Bienvenue sur notre site. Pour commencer la visite, merci de mettre à jour la base de donnée en cliquant sur le bouton ci-dessous</span>
    <br>
    <button style="margin:15px 0" type="submit" name="save" class="btn btn-dark">Load and Save in Database</button>
      
    </div>
      
    </form>  
      </div>
    </main>
  </div>
</div>
% include('scripts.tpl', title='Scripts')
		</body>
</html>
