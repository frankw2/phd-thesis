# Called by Applier layer after applying log to disk.
def disklog_truncate(txn):
    header = disk_read(CommitBlock)
    header.previous_len = header.len
    header.len = 0
    disk_write(CommitBlock, header)
    disk_sync()

# Called by Applier layer, which guarantees that there's enough space.
def disklog_append(txn):
    header = disk_read(CommitBlock)
    write_packed_addresses(LogDescStart, header.len, txn)
    pos = LogDataStart + header.len
    for (a, v) in txn.iteritems():
        disk_write(pos, v)
        header.checksum = hash(header.checksum || a || v)
        pos += 1
    header.previous_len = header.len
    header.len = header.len + len(txn)
    disk_write(CommitBlock, header)
    disk_sync()

def disklog_readlog(nr):
    checksum = hash(0)
    log = []
    for i in range(0, nr):
        a = read_packed_address(LogDescStart, i)
        v = disk_read(LogDataStart + i)
        checksum = hash(checksum || a || v)
        log.append((a, v))
    return (checksum, log)

def disklog_recover():
    header = disk_read(CommitBlock)
    (checksum, log) = disklog_readlog(header.len) 
    if checksum != header.checksum:
        (checksum, log) = disklog_readlog(header.previous_len) 
        header.checksum = checksum
        header.len = header.previous_len
        disk_write(CommitBlock, header)
        disk_sync()
    return log
