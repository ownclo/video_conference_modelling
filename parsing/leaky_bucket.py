
def leaky_bucket_loss(drain_rate, bucket_size, seq):
#    assert drain_rate <= bucket_size

    num_loss = 0
    content = 0

    for x in seq:
        content += x
        if content > bucket_size:
            loosed = content - bucket_size
            content = bucket_size
            num_loss += loosed
        content = drain_out(content, drain_rate)

    return num_loss

def drain_out(content, drain_rate):
    delta = content - drain_rate
    if delta < 0:
        return 0
    else:
        return delta

if __name__ == '__main__':
    seq = [1,2,3,1,2,3]
    drain_rate = 1
    bucket_size = 2

    num_loss = leaky_bucket_loss(drain_rate, bucket_size, seq)
    print num_loss
