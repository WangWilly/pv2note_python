import json
import numpy as np
import matplotlib.pyplot as plt


# x_min, x_max, y_min, y_max = 0, 7, 54, 74
def pvPlot(sample_pitch, sample_time):
    plt.plot(sample_time, sample_pitch, 'r.')
    # plt.axis([0, 7, 54, 74])

def pvPlay(is_value, sample_time):
    plt.bar(sample_time, is_value, width=0.05)

def notePlot(start_t: list, end_t: list, note: list):
    for (s, e, n) in zip(start_t, end_t, note):
        plt.plot([float(s), float(e)], [float(n), float(n)], color='b')
        plt.plot(s, n, 'b>')
    # plt.axis([0, 7, 54, 74])

def pv2note(pitch, time, threshold=1.5):
    assert len(pitch)==len(time) and threshold>0
    segement_list = []
    start_t_list  = []
    end_t_list    = []
    note_list     = []
    base_val = 0
    start_time = 0
    for val, now_time in zip(pitch, time):
        if len(segement_list) == 0 and val != 0:
            segement_list.append(val)
            base_val = val
            start_time = now_time
        elif abs(val - base_val) < threshold and val != 0:
            segement_list.append(val)
        elif val != 0:
            start_t_list.append(start_time)
            end_t_list.append(now_time)
            note_list.append(np.median(segement_list))
            start_time = now_time
            segement_list = [val]
            base_val = val
        else:
            if len(segement_list) > 0:
                start_t_list.append(start_time)
                end_t_list.append(now_time)
                note_list.append(np.median(segement_list))
                segement_list = []
    if len(segement_list) > 0:
        start_t_list.append(start_time)
        end_t_list.append(now_time)
        note_list.append(np.median(segement_list))
    return start_t_list, end_t_list, note_list


if __name__ == "__main__":
    with open('./MIR-ST500/6/6_feature.json' , 'r') as reader:
        jf = json.loads(reader.read())

    pitch = np.array(jf['vocal_pitch'])
    time = np.array(jf['time'])

    is_value = [(v) and 1 or 0 for v in pitch]
    pvPlay(is_value, time)
    plt.show()

    s, e, n = pv2note(pitch, time)
    pvPlot(pitch, time)
    notePlot(s,e,n)
    plt.show()


    index = (time >= 27) & (time <= 33.5)
    sample_pitch = pitch[index]
    sample_time = time[index]-27

    is_value = [(v) and 1 or 0 for v in sample_pitch]
    pvPlay(is_value, sample_time)
    
    s, e, n = pv2note(sample_pitch, sample_time)
    pvPlot(sample_pitch, sample_time)
    notePlot(s,e,n)
    plt.show()

    with open('./MIR-ST500/6/6_groundtruth.txt', 'r') as f:
        gt = [line.strip().split() for line in f.readlines()]
        gt = np.array([[float(i) for i in vals] for vals in gt])
    index = (gt[:,0] >= 27) & (gt[:,1] <= 33.5)
    notePlot(gt[index,0], gt[index,1], gt[index,2])
    plt.axis([27, 33.5, 54, 74])
    plt.show()