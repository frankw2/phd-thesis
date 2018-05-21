#!/usr/bin/python2

import sys, collections

counts = collections.defaultdict(int)

breakdown = [
  ( 'FSCQ and CHL infrastructure',
    [ 'Word.v', 'Bytes.v', 'Rounding.v',
      'Hoare.v', 'BasicProg.v', 'GenSep.v', 'GenSepN.v',
      'Idempotent.v', 'ListPred.v',
      'MemMatch.v', 'Pred.v', 'PredCrash.v', 'Mem.v',
      'Prog.v', 'ProgMonad.v', 'AsyncDisk.v',
      'MemPred.v',
      'SepAuto.v', 'WordAuto.v', 'Nomega.v', 'GenSepAuto.v',
      'Rec.v', 'RecArrayUtils.v', 'RecArray.v', 'AsyncRecArray.v', 'Array.v',
      'FileRecArray.v', 'DirUtil.v',
      'Balloc.v',
    ] ),
  ( 'Hashing semantics',
    [ 'Hashmap.v', 'HashmapProg.v',
    ] ),
  ( 'General data structures',
    [ 'ListUtils.v', 'MapUtils.v', 'NEList.v', 'StringUtils.v', 'TreeUtils.v',
    ] ),
  ( 'Buffer cache',
    [ 'ReadCacheX.v', 'Cache.v', 'ReadCache.v', ] ),
  ( 'Write-ahead log',
    [ 'DiskLogHash.v', 'LogReplay.v', 'MemLog.v', 'GroupLog.v', 'Log.v',
      'LogRecArray.v', 'DiskSet.v',
    ] ),
  ( 'Inodes and files',
    [ 'Inode.v', 'BFile.v', 'BlockPtr.v' ] ),
  ( 'Directories',
    [ 'DirName.v', 'Dir.v', 'DirTree.v', 'TreeCrash.v', ] ),
  ( "\sys's top-level API",
    [ 'SuperBlock.v', 'FSLayout.v', 'AsyncFS.v', 'AsyncFSRecover.v', ] ),
  ( 'ignore',
    [ 'ExampleMemLog.v', 'Extraction.v', 'ExtractJSON.v',
      'ExtrHaskellPrelude.v', 'KV.v', 'Lock.v',
      'ProposalExample.v', 'Scratch.v', 'Testprog.v',
      'Errno.v', 'Concur.v', 'ProgConcur.v', 'RG.v', 'CSL.v',
      'App.v', 'SepAuto2.v', 'ExampleBlockRecover.v', 'ExampleChecksumLog.v',
      'ExtractHaskell.v', 'ExtractOcaml.v', 'FastByteFile.v', 'NewExtract.v',
      'RecoverExample.v',
      ## In progress
      'WordZ.v',
      'AtomicCp.v',
      'AByteFile.v',
      'DirSep.v',
      'TreeSeq.v',
      'VBConv.v',
      # Unused
      'ByteFile.v',
      'WritebackCache.v',
      'Compare.v',
      'DestructPair.v',
      'DiskLog.v',
    ] ),
]

for l in sys.stdin.readlines():
  (num, filename) = l.strip().split()
  num = int(num)
  if filename == 'total':
    continue
  filename = filename.split('/')[-1]
  found = False
  for (component, filenames) in breakdown:
    if filename in filenames:
      if found:
          print >>sys.stderr, "Found %s twice" % filename
      assert not found
      counts[component] += num
      found = True
  if not found:
    print >>sys.stderr, "Not found: %s" % filename
    assert found

def fmt(x):
  return "{:,}".format(x)

total = 0
for (component, _) in breakdown:
  if component == 'ignore':
    continue
  print '%s & %s \\\\' % (component, fmt(counts[component]))
  total += counts[component]
print '\\midrule'
print 'Total & %s ' % fmt(total)
