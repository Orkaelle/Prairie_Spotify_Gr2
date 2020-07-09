<!doctype html>
<html lang="en">
  <head>
    % include('head.tpl', title='Head')
  </head>
  <body>
  
<div class="container-fluid">
    <form action="/popularity_xgb" method="get">
        <div class="row">
            
            % include('nav.tpl', title='Navigation')

            <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-md-4">
            <h2>Prédiction de la popularité - algorithme de Farida</h2>
            
            <div class="table-responsive">
                <table class="table table-striped table-sm">
                <thead>
                    <tr>
                    <th style="width:100%"></th>
                    </tr>
                </thead>
                <tbody>
                    % for graph in graphs:
                    <tr>
                        <td>
                            <img src="get/prediction/picture/{{graph}}"></img>
                        </td>
                    </tr>
                    % end
                    <tr>
                        <td>
                            <b>Prédictions:</b>
                            </br>
                            <table>
                                <thead>
                                    <tr>
                                    <th style="width:auto">itération</th>
                                    <th style="width:100%">résultat</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    % i=0
                                    % for prediction in predictions:
                                    % i = i + 1
                                    <tr>
                                        <td>
                                            {{i}}
                                        </td>
                                        <td>
                                            {{prediction}}
                                        </td>
                                    </tr>
                                    % end
                                </tbody>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td><b>Erreur</b> : {{error}} </td>
                    <td>
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