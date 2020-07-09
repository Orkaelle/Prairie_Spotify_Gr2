<!doctype html>
<html lang="en">
  <head>
    % include('head.tpl', title='Head')
  </head>
  <body>
% include('top_nav.tpl', title='Top navigation')
<div class="container-fluid">
    <form action="/popularity_xgb" method="get">
        <div class="row">
            
            % include('nav.tpl', title='Navigation')

            <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-md-4">
            <h2>Prédiction de la popularité avec XgBoost</h2>
            
            <div class="table-responsive">
                <table class="table table-striped table-sm">
                <thead>
                    <tr>
                    <th style="width:auto">Titre</th>
                    <th style="width:auto">Playlist</th>
                    <th style="width:100%"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td>
                        <input type="text" name="song" maxlength="30" value="{{song}}"/>
                    </td>
                    <td>
                        <select name="playlist">
                            % for item in playlists:
                                <option value="{{item[0]}}" {{!'selected="selected"' if item[2] == 1 else ""}}>{{item[1]}}</option>
                            % end
                        </select>
                    </td>
                    <td>
                        <button type="submit" style="background:transparent; border: none" title="lancer la recherche">
                        <span data-feather="search"></span>
                        </button>
                    </td>
                    </tr>
                    <tr>
                    <td>
                        <span>prediction calculated between {{prediction_min}}% and {{prediction_max}}%</span>
                    </td>
                    </tr>
                    
                </tbody>
                </table>
            </div>
            </main>
        </div>
    </form>
</div>
% include('scripts.tpl', title='Scripts')

<script type="text/javascript">

    
</script>
</body>
</html>