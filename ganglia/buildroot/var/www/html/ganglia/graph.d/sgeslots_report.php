<?php

/* Sample report template */

/* Instructions for adding custom reports

1) Reports should have a primary function named:  "<yourtesthere>_report".
   This function will be called from the graph.php script automatically.

2) The *_report script should return an array that contains at least the
   variables listed below.  Several have been pre-populated, and may not
   need to be changed.
   However, you will have to alter at least these:  $series, $title, and
   $vertical_label

3) An array variable is passed to the function in order to make sure that
   certain variables are available for use.  This is PASSED BY REFERENCE
   and CAN BE CHANGED by your report function.

NOTE:  These are all actually keys in a hash, not specific variables by
       themselves.

A full list of variables that will be used:

    $series          (string: holds the meat of the rrdgraph definition)
    $title           (string: title of the report)
    $vertical_label  (string: label for Y-Axis.)

    $start           (string: Start time of the graph, can usually be
                              left alone)
    $end             (string: End time of the graph, also can usually be
                              left alone)

    $width           (strings: Width and height of *graph*, the actual image
    $height                    will be slightly larger due to text elements
                               and padding.  These are normally set
                               automatically, depending on the graph size
                               chosen from the web UI)

    $upper-limit     (strings: Maximum and minimum Y-value for the graph.
    $lower-limit               RRDtool normally will auto-scale the Y min
                               and max to fit the data.  You may override
                               this by setting these variables to specific
                               limits.  The default value is a null string,
                               which will force the auto-scale behavior)

    $color           (array: Sets one or more chart colors.  Usually used
                             for setting the background color of the chart.
                             Valid array keys are BACK, CANVAS, SHADEA,
                             SHADEB, FONT, FRAME and ARROW.  Usually,
                             only BACK is set).

    $extras          (Any other custom rrdtool commands can be added to this
                      variable.  For example, setting a different --base
                      value or use a --logarithmic scale)

For more information and specifics, see the man page for 'rrdgraph'.

*/

function graph_sgeslots_report ( &$rrdtool_graph ) {

/*
 * this is just the cpu_report (from revision r920) as an example, but
 * with extra comments
 */

// pull in a number of global variables, many set in conf.php (such as colors
// and $rrd_dir), but other from elsewhere, such as get_context.php

    global $context,
           $cpu_idle_color,
           $cpu_nice_color,
           $cpu_system_color,
           $cpu_user_color,
           $cpu_num_color,
           $cpu_wio_color,
           $hostname,
           $range,
           $rrd_dir,
           $size,
           $strip_domainname;

    if ($strip_domainname) {
       $hostname = strip_domainname($hostname);
    }

    //
    // You *MUST* set at least the 'title', 'vertical-label', and 'series'
    // variables otherwise, the graph *will not work*.
    //
    $title = 'SGE Slots';
    if ($context != 'host') {
       //  This will be turned into: "Clustername $TITLE last $timerange",
       //  so keep it short
       $rrdtool_graph['title']  = $title;
    } else {
       $rrdtool_graph['title']  = "$hostname $title last $range";
    }
    $rrdtool_graph['vertical-label'] = 'SGE Slots';
    // Fudge to account for number of lines in the chart legend
    $rrdtool_graph['height']        += ($size == 'medium') ? 28 : 0;
    // $rrdtool_graph['upper-limit']    = '100';
    $rrdtool_graph['lower-limit']    = '0';
    $rrdtool_graph['extras']         = '--rigid';

    /*
     * Here we actually build the chart series.  This is moderately complicated
     * to show off what you can do.  For a simpler example, look at
     * network_report.php
     */
    if($context != "host" ) {
        $series ="'DEF:slots_total=${rrd_dir}/slots_total.rrd:sum:AVERAGE' "
        . "'DEF:slots_used=${rrd_dir}/slots_used.rrd:sum:AVERAGE' "
        . "'AREA:slots_used#$cpu_user_color:Slots Used' "
        . "'LINE2:slots_total#$cpu_num_color:Slots Total' ";

    } else {
        // Context is "host"
        $series ="'DEF:slots_total=${rrd_dir}/slots_total.rrd:sum:AVERAGE' "
        . "'DEF:slots_used=${rrd_dir}/slots_used.rrd:sum:AVERAGE' "
        . "'AREA:slots_used#$cpu_user_color:Slots Used' "
        . "'LINE2:slots_total#$cpu_nice_color:Slots Total' ";
    }

    // We have everything now, so add it to the array, and go on our way.
    $rrdtool_graph['series'] = $series;

    return $rrdtool_graph;
}

?>
