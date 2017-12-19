HMM
#MLE estimate
python MLETrain.py input_file_name q_mle_filename e_mle_filename
#greedy
python GreedyTag.py input_file_name q_mle_filename e_mle_filename output_file_name
#viterbi
python HMMTag.py input_file_name q_mle_filename e_mle_filename output_file_name


MEMM
#train
ExtractFeatures corpus_file features_file
ConvertFeatures features_file feature_vecs_file feature_map_file
java -cp liblinear-2.11.jar de.bwaldvogel.liblinear.Train -s 0 -c 0.001 feature_vecs_file model
!!! TrainSolver.py is not in use !!!
#greedy
python GreedyMaxEntTag.py input_file_name model_file_name output_file_name feature_map_file
#viterbi
python MEMMTag.py input_file_name model_file_name output_file_name feature_map_file