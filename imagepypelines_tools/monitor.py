from flask import Flask
import json
app = Flask(__name__)


MONITOR = \
"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>ImagePypelines Monitor</title>

    <!-- THEMES -->
    <link href="css/simplex.min.css" rel="stylesheet">
  </head>
  <body>
  {bars}
  </body>
 </html>

"""
BAR_TEMPLATE = \
"""
<h2>{pipeline}</h2>
<div class="progress">
  <div class="progress-bar progress-bar-stripe progress-bar-animated" role="progressbar" aria-valuenow="{progress}" aria-valuemin="0" aria-valuemax="100">{label}</div>
</div>
<br>
"""
# keys: pipeline_name, progress, label

@app.route('/',methods=["POST"])
def update_pipeline():
    """
    request.data -->
    json encoded dictionary with the following

        {
        "pipeline1":{
                    'current_block_name':<current_block_name>
                    'current_block_index':<current_block_index>
                    'num_blocks':<num_blocks>
                    'current_block_avg_processing_time':<processing_time>,
                    'num_in':<num_in>,
                    'num_out':<num_out>,
                    'total_in':<total_in>,
                    'total_out':<total_out>,
                    'training_time':<training_time>,
                    }
        "pipeline2":{
                    'current_block_name':<current_block_name>
                    'current_block_index':<current_block_index>
                    'num_blocks':<num_blocks>
                    'current_block_avg_processing_time':<processing_time>,
                    'num_in':<num_in>,
                    'num_out':<num_out>,
                    'total_in':<total_in>,
                    'total_out':<total_out>,
                    'training_time':<training_time>,
                    }
        }
    """
    updates = json.loads(request.data)
    bars_string = ""
    for pipeline in sorted( updates.keys() ):
        progress = updates[pipeline]['current_block_index'] / updates[pipeline]['num_blocks'] * 100
        bars_string += BAR_TEMPLATE.format(pipeline=pipeline,
                                            progress = progress,
                                            val = str( round(progress,0) ) + r'%'
                                            )

    return MONITOR.format(bars=bars_string)




if __name__ == "__main__":
    app.run()
