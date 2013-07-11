#!/bin/bash

RunRetentionDays=130
ThumbnailImagesRetentionDays=38
AnalysisRetentionDays=24

function RecurseDirectory {
  
  # Master loop over the contents of the directory
  for i in "$1"/*; do
    if [ -d "$i" ]; then
      BaseName=${i##*/}  
      if [ "$BaseName" == "Focus" ]; then
        echo Deleting "$2" day old Focus folder "$i"
        qsub -cwd -b y -V -p -1023 rm -rf "$i"
        continue
      elif [ "$BaseName" == "AFCalImages*" ]; then
        echo Deleting "$2" day old AFCalImages folder "$i"
        qsub -cwd -b y -V -p -1023 rm -rf "$i"
        continue
      elif [ "$BaseName" == "Calibration*" ]; then
        echo Deleting "$2" day old images in Calibration folder "$i"
        rm "$i"/*.tif
        continue
      elif [ "$BaseName" == "Thumbnail_Images" ] && [ "$2" -gt "$ThumbnailImagesRetentionDays" ]; then
        echo Deleting "$2" day old ThumbnailImages folder "$i"
        qsub -cwd -b y -V -p -1023 rm -rf "$i"
        continue
      elif [ "$BaseName" == "DebugPixels" ] && [ "$2" -gt "$ThumbnailImagesRetentionDays" ]; then
        echo Deleting "$2" day old DebugPixels folder "$i"
        qsub -cwd -b y -V -p -1023 rm -rf "$i"
        continue
      fi

      # Do the export compression if the alignment has finished
      if [ -f "$i"/finished.txt ]; then
        for j in "$i"/s_*_export.txt; do
          if [ -f "$j" ]; then
            qsub -cwd -b y -V -p -1023 gzip "$j"
            echo Gzipping "$2" day old export file "$k"
          fi
        done
      fi

      rm "$i"/*_L*_R*_*.fastq.gz
      rm "$i"/*_L*_R*_*.fastq
      rm "$i"/s*_qseq.txt
      rm "$i"/s*_seq.txt
      rm "$i"/s*_prb.txt
      rm "$i"/s*_qval.txt.gz
      rm "$i"/s*.bcl
      rm "$i"/s*.filter
      rm "$i"/s*_int.txt.p.gz
      rm "$i"/s*_nse.txt.p.gz
      rm "$i"/s*_int.txt.gz
      rm "$i"/s*_nse.txt.gz
      rm "$i"/s*_sig2.txt.gz
      rm "$i"/s*.cif
      rm "$i"/s*.dif
      rm "$i"/s*.locs
      rm "$i"/s*.clocs
      rm "$i"/s*.ctr
      rm "$i"/s*_pos.txt
      rm "$i"/s*_eland_query.txt
      rm "$i"/s*_calsaf.txt
      rm "$i"/s*_eland_extended.txt
      rm "$i"/s*_eland_extended.txt.gz
      rm "$i"/s*_eland_multi.txt
      rm "$i"/s*_eland_multi.txt.gz
      rm "$i"/s*_frag.txt
      rm "$i"/s*_score_files.txt
      rm "$i"/s*_sequence.txt
      rm "$i"/s*_sequence.txt.gz
      rm "$i"/s*_sorted.txt
      rm "$i"/s*_sorted.txt.gz
      rm "$i"/s*_reanomraw.txt
      rm "$i"/s*_anomaly.txt

      RecurseDirectory "$i" "$2"
    fi
  done

}

function SearchRunDirectory {

  # Master loop over the contents of the run directory
  for i in "$1"/*; do
    if [ -d "$i" ]; then # check that this is a direcotry
      if [ -f "$i"/saverundata.txt ]; then
        # Don't delete anything if the saverundata.txt file is present
        echo Save run folder "$i"
      else
        # Figure out how old the run is
        RunFolder=${i##*/} # get everything after last /
        RunYear=${RunFolder:0:2} # first two digits are year
        RunYear=${RunYear#0} # remove leading zeros
        RunMonth=${RunFolder:2:2} # next two digits are month
        if [[ $RunMonth == *-* ]] # special handling for Bolt run folder format of YY-MM-DD
        then
          RunMonth=${RunFolder:3:2}
        fi
        RunMonth=${RunMonth#0} # remove leading zeros
        RunDay=${RunFolder:4:2} # last 2 digits are day
        if [[ $RunDay == *-* ]] # special handling for Bolt run folder format YY-MM-DD
        then
          RunDay=${RunFolder:6:2}
        fi
        RunDay=${RunDay#0} # remove leading zeros
        CurrentYear=`date +%y`
        CurrentYear=${CurrentYear#0}
        CurrentMonth=`date +%m`
        CurrentMonth=${CurrentMonth#0}
        CurrentDay=`date +%d`
        CurrentDay=${CurrentDay#0}
        # check that directory has digits for year, month, and day
        if echo "$RunYear""$RunMonth""$RunDay" | egrep "^[0-9]+$"; then
          DaysOld=$(( ($CurrentYear - $RunYear) * 365 + ($CurrentMonth - $RunMonth) * 30 + $CurrentDay - $RunDay ))
          if [ "$DaysOld" -gt "$2" ] && [ -d "$i"/Images ]; then
            echo Deleting "$DaysOld" day old Images folder "$i"/Images
            qsub -cwd -b y -V -p -1023 rm -rf "$i"/Images
          fi
          if [ "$DaysOld" -gt "$RunRetentionDays" ]; then
            echo Deleting "$DaysOld" day old run folder "$i"
            qsub -cwd -b y -V -p -1023 rm -rf "$i"
          elif [ "$DaysOld" -gt "$AnalysisRetentionDays" ]; then
            echo Searching "$DaysOld" day old run folder "$i"
            RecurseDirectory "$i" "$DaysOld"
          else
            echo No action required for "$DaysOld" day old run folder "$i"
          fi 
        fi # end if on check that it is a run folder
      fi # end if on check for saverundata.txt file
    fi # end if on check for directory
  done # end for loop over contents of run directory

}

echo "Starting data deletion policy at " `date`
echo `df -h | grep bruno`
echo `df -h | grep harmonia`

SearchRunDirectory "$1" "$2"

echo "Ending data deletion policy at " `date`
echo `df -h | grep bruno`
echo `df -h | grep harmonia`
