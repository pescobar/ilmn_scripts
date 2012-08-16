<?php

function graph_sgeslots_report ( &$rrdtool_graph ) {

    global $context,
           $hostname,
           $cpu_user_color,
           $cpu_num_color,
           $range,
           $rrd_dir,
           $size,
           $graphreport_stats,
           $strip_domainname;

    if ($strip_domainname) {
       $hostname = strip_domainname($hostname);
    }

    $title = 'SGE Slots';
    $rrdtool_graph['height'] += ($size == 'medium') ? 28 : 0;
    if ( $graphreport_stats ) {
        $rrdtool_graph['height'] += ($size == 'medium') ? 52 : 0;
        $rmspace = '\\g';
    } else {
        $rmspace = '';
    }

    if ($context != 'host') {
       $rrdtool_graph['title']  = $title;
    } else {
       $rrdtool_graph['title']  = "$hostname $title last $range";
    }
    $rrdtool_graph['vertical-label'] = 'SGE Slots';
    $rrdtool_graph['height']        += ($size == 'medium') ? 28 : 0;
    $rrdtool_graph['lower-limit']    = '0';
    $rrdtool_graph['extras']         = '--rigid';
    $rrdtool_graph['extras'] .= ($graphreport_stats == true) ? ' --font LEGEND:7' : '';

    $series ="'DEF:slots_total=${rrd_dir}/slots_total.rrd:sum:AVERAGE' "
    . "'DEF:slots_used=${rrd_dir}/slots_used.rrd:sum:AVERAGE' "
    . "'AREA:slots_used#$cpu_user_color:Used${rmspace}' ";

    if ( $graphreport_stats ) {
      $series .= "CDEF:slotsused_pos=slots_used,0,INF,LIMIT "
              . "VDEF:slotsused_last=slotsused_pos,LAST "
              . "VDEF:slotsused_min=slotsused_pos,MINIMUM "
              . "VDEF:slotsused_avg=slotsused_pos,AVERAGE "
              . "VDEF:slotsused_max=slotsused_pos,MAXIMUM "
              . "GPRINT:'slotsused_last':' ${space1}Now\:%6.1lf%s' "
              . "GPRINT:'slotsused_min':' ${space1}Min\:%6.1lf%s${eol1}' "
              . "GPRINT:'slotsused_avg':' ${space1}Avg\:%6.1lf%s' "
              . "GPRINT:'slotsused_max':' ${space1}Max\:%6.1lf%s\\l' ";
    }

    $series .= "'LINE2:slots_total#$cpu_num_color:Total${rmspace}' ";

    if ( $graphreport_stats ) {
      $series .= "CDEF:slotstotal_pos=slots_total,0,INF,LIMIT "
              . "VDEF:slotstotal_last=slotstotal_pos,LAST "
              . "VDEF:slotstotal_min=slotstotal_pos,MINIMUM "
              . "VDEF:slotstotal_avg=slotstotal_pos,AVERAGE "
              . "VDEF:slotstotal_max=slotstotal_pos,MAXIMUM "
              . "GPRINT:'slotstotal_last':' ${space1}Now\:%6.1lf%s' "
              . "GPRINT:'slotstotal_min':' ${space1}Min\:%6.1lf%s${eol1}' "
              . "GPRINT:'slotstotal_avg':' ${space1}Avg\:%6.1lf%s' "
              . "GPRINT:'slotstotal_max':' ${space1}Max\:%6.1lf%s\\l' ";
    }

    $rrdtool_graph['series'] = $series;

    return $rrdtool_graph;
}

?>
