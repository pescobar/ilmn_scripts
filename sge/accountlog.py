# SGE log parser
# ($SGE_ROOT/default/common/accounting)

# sge accounting file fields:
#
# qname:hostname:group:owner:job_name:job_number:account:priority:
# submission_time:start_time:end_time:failed:exit_status:ru_wallclock:
# ru_utime:ru_stime:ru_maxrss:ru_ixrss:ru_ismrss:ru_idrss:ru_isrss:
# ru_minflt:ru_majflt:ru_nswap:ru_inblock:ru_oublock:ru_msgsnd:ru_msgrcv:
# ru_nsignals:ru_nvcsw:ru_nivcsw:project:department:granted_pe:slots:
# task_number:cpu:mem:io:category:iow:pe_taskid:maxvmem:arid:
# ar_submission_time
import os

# SGE
try:
  '''if SGE_ROOT isn't set, pretty good odds no SGE vars are set'''
  os.environ["SGE_ROOT"]
except:
  os.environ["SGE_ROOT"] = "/opt/gridengine"
  os.environ["SGE_CELL"] = "default"
  os.environ["SGE_ARCH"] = "lx26-amd64"
  os.environ["SGE_EXECD_PORT"] = "537"
  os.environ["SGE_QMASTER_PORT"] = "536"

sge_root = os.environ["SGE_ROOT"]
sge_cell = os.environ["SGE_CELL"]

def parse_sge_accountlog():
  fd = open(sge_root + "/" + sge_cell + "/common/accounting")
  jobs = {}
  for line in fd.readlines():
    if not line.startswith('#'):
      [ qname, host, group, owner, job_name, job_number, account, priority,
      submission_time, start_time, end_time, failed, exit_status, ru_wallclock,
      ru_utime, ru_stime, ru_maxrss, ru_ixrss, ru_ismrss, ru_idrss, ru_isrss,
      ru_minflt, ru_majflt, ru_nswap, ru_inblock, ru_oublock, ru_msgsnd, ru_msgrcv,
      ru_nsignals, ru_nvcsw, ru_nivcsw, project, department, granted_pe, slots,
      task_number, cpu, mem, io, category, iow, pe_taskid, maxvmem, arid, 
      ar_submission_time ] = line.split(":")

      # total jobs per queue
      try:
        jobs[qname] = jobs[qname] + 1
      except:
        jobs[qname] = 1


  return jobs

queues = parse_sge_accountlog()
for k, v in queues.iteritems():
  print k, v
