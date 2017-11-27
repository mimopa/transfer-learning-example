import tensorflow as tf
import sys,os

# config - TensorFlow model file
LABEL = "model/retrained_labels.txt"
GRAPH = "model/retrained_graph.pb"

class ImageRec():
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.label_lines = [line.rstrip() for line 
                           in tf.gfile.GFile(os.path.join(self.dir_path, LABEL))]
        self.create_graph()
        self.sess = tf.Session()

    def create_graph(self):
        with tf.gfile.FastGFile(os.path.join(self.dir_path, GRAPH), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

    def run(self, image_path):
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()

        # feed the image_data as input to the graph and get first prediction
        softmax_tensor = self.sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = self.sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
        
        # sort to labels of  prediction in order of confidence
        top = predictions[0].argsort()[-len(predictions[0]):][::-1]
        
        # make results for display
        image_info = []
        for node_id in top:
            label = self.label_lines[node_id]
            score = round(predictions[0][node_id] * 100.0, 2)
            print('%s (score = %.5f)' % (label, score))

            score_info = {}
            score_info['name']=label
            score_info['score']=score
            image_info.append(score_info)

        return image_info