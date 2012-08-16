<?php

function graph_sgeslots_report ( &$rrdtool_graph ) {

    global $context,
           $hostname,
           $cpu_user_color,
           $cpu_num_color,
           $range,
           $rrd_dir,
           $size,
           $strip_domainname;

    if ($strip_domainname) {
       $hostname = strip_domainname($hostname);
    }

    $title = 'SGE Slots';
    if ($context != 'host') {
       $rrdtool_graph['title']  = $title;
    } else {
       $rrdtool_graph['title']  = "$hostname $title last $range";
    }
    $rrdtool_graph['vertical-label'] = 'SGE Slots';
    $rrdtool_graph['height']        += ($size == 'medium') ? 28 : 0;
    $rrdtool_graph['lower-limit']    = '0';
    $rrdtool_graph['extras']         = '--rigid';

    if($context != "host" ) {
        $series ="'DEF:slots_total=${rrd_dir}/slots_total.rrd:sum:AVERAGE' "
        . "'DEF:slots_used=${rrd_dir}/slots_used.rrd:sum:AVERAGE' "
        . "'AREA:slots_used#$cpu_user_color:Slots Used' "
        . "'LINE2:slots_total#$cpu_num_color:Slots Total' ";

    }

    $rrdtool_graph['series'] = $series;

    return $rrdtool_graph;
}

?>
