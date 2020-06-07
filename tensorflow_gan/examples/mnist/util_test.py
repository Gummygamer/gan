# coding=utf-8
# Copyright 2020 The TensorFlow GAN Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for mnist.util."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow.compat.v1 as tf
from tensorflow_gan.examples.mnist  import util

mock = tf.test.mock


# pylint: disable=line-too-long
# This is a real digit `5` from MNIST.
REAL_DIGIT = [[-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.9765625, -0.859375, -0.859375, -0.859375, -0.015625, 0.0625, 0.3671875, -0.796875, 0.296875, 0.9921875, 0.9296875, -0.0078125, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.765625, -0.71875, -0.265625, 0.203125, 0.328125, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.7578125, 0.34375, 0.9765625, 0.890625, 0.5234375, -0.5, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.6171875, 0.859375, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.9609375, -0.2734375, -0.359375, -0.359375, -0.5625, -0.6953125, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.859375, 0.7109375, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.546875, 0.421875, 0.9296875, 0.8828125, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.375, 0.21875, -0.1640625, 0.9765625, 0.9765625, 0.6015625, -0.9140625, -1.0, -0.6640625, 0.203125, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.890625, -0.9921875, 0.203125, 0.9765625, -0.296875, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 0.0859375, 0.9765625, 0.484375, -0.984375, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.9140625, 0.484375, 0.9765625, -0.453125, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.7265625, 0.8828125, 0.7578125, 0.25, -0.15625, -0.9921875, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.3671875, 0.875, 0.9765625, 0.9765625, -0.0703125, -0.8046875, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.6484375, 0.453125, 0.9765625, 0.9765625, 0.171875, -0.7890625, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.875, -0.2734375, 0.96875, 0.9765625, 0.4609375, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 0.9453125, 0.9765625, 0.9453125, -0.5, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.640625, 0.015625, 0.4296875, 0.9765625, 0.9765625, 0.6171875, -0.984375, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.6953125, 0.15625, 0.7890625, 0.9765625, 0.9765625, 0.9765625, 0.953125, 0.421875, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.8125, -0.109375, 0.7265625, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.5703125, -0.390625, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.8203125, -0.484375, 0.6640625, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.546875, -0.3671875, -0.984375, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.859375, 0.3359375, 0.7109375, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.5234375, -0.375, -0.9296875, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -0.5703125, 0.34375, 0.765625, 0.9765625, 0.9765625, 0.9765625, 0.9765625, 0.90625, 0.0390625, -0.9140625, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, 0.0625, 0.9765625, 0.9765625, 0.9765625, 0.65625, 0.0546875, 0.03125, -0.875, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]]
ONE_HOT = [[0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]]

# Uniform noise in [-1, 1].
FAKE_DIGIT = [[0.778958797454834, 0.8792028427124023, 0.07099628448486328, 0.8518857955932617, -0.3541288375854492, -0.7431280612945557, -0.12607860565185547, 0.17328786849975586, 0.6749839782714844, -0.5402040481567383, 0.9034252166748047, 0.2420203685760498, 0.3455841541290283, 0.1937558650970459, 0.9989571571350098, 0.9039363861083984, -0.955411434173584, 0.6228537559509277, -0.33131909370422363, 0.9653763771057129, 0.864208459854126, -0.05056142807006836, 0.12686634063720703, -0.09225749969482422, 0.49758028984069824, 0.08698725700378418, 0.5533185005187988, 0.20227980613708496], [0.8400616645812988, 0.7409703731536865, -0.6215496063232422, -0.53228759765625, -0.20184636116027832, -0.8568699359893799, -0.8662903308868408, -0.8735041618347168, -0.11022663116455078, -0.8418543338775635, 0.8193502426147461, -0.901512622833252, -0.7680232524871826, 0.6209826469421387, 0.06459426879882812, 0.5341305732727051, -0.4078702926635742, -0.13658642768859863, 0.6602437496185303, 0.848508358001709, -0.23431801795959473, 0.5995683670043945, -0.9807922840118408, 0.2657158374786377, -0.8068397045135498, 0.2438051700592041, -0.2116842269897461, 0.011460304260253906], [0.00040912628173828125, -0.058798789978027344, 0.3239307403564453, 0.5040378570556641, -0.03192305564880371, -0.4816470146179199, -0.14559340476989746, -0.9231269359588623, -0.6602556705474854, -0.2537086009979248, -0.11059761047363281, -0.8174862861633301, 0.6180260181427002, 0.7245023250579834, 0.5007762908935547, -0.1575303077697754, -0.0167086124420166, 0.7173266410827637, 0.1126704216003418, -0.9878268241882324, 0.4538843631744385, -0.4422755241394043, -0.7899672985076904, 0.7349567413330078, -0.4448075294494629, -0.7548923492431641, -0.5739786624908447, 0.30504918098449707], [-0.8488152027130127, 0.43424463272094727, 0.7724254131317139, 0.43314504623413086, 0.7352848052978516, -0.26010799407958984, 0.43951940536499023, -0.7642686367034912, -0.657184362411499, -0.9933960437774658, -0.47258639335632324, 0.10390830039978027, 0.11454653739929199, -0.6156411170959473, -0.23431062698364258, -0.6897118091583252, -0.5721850395202637, -0.3574075698852539, 0.13927006721496582, -0.6530766487121582, 0.32231855392456055, 0.6294634342193604, 0.5507853031158447, -0.4867420196533203, 0.4329197406768799, 0.6168341636657715, -0.8720219135284424, 0.8639121055603027], [0.02407360076904297, -0.11185193061828613, -0.38637852668762207, -0.8244953155517578, -0.648916482925415, 0.44907593727111816, -0.368192195892334, 0.0190126895904541, -0.9450500011444092, 0.41033458709716797, -0.7877917289733887, 0.617938756942749, 0.551692008972168, -0.48288512229919434, 0.019921541213989258, -0.8765170574188232, 0.5651748180389404, 0.850874662399292, -0.5792787075042725, 0.1748213768005371, -0.6905481815338135, -0.521310567855835, 0.062479496002197266, 0.17763280868530273, -0.4628307819366455, 0.8870463371276855, -0.8685822486877441, -0.29169774055480957], [-0.14687561988830566, 0.8801963329315186, 0.11353135108947754, -0.6009430885314941, 0.8818719387054443, -0.8621203899383545, -0.48749589920043945, 0.5224916934967041, 0.7050364017486572, -0.9968757629394531, 0.7235188484191895, 0.662771463394165, 0.588390588760376, -0.9624209403991699, 0.39203453063964844, -0.2210233211517334, 0.9266352653503418, -0.9132544994354248, -0.5175333023071289, 0.7251780033111572, 0.3030557632446289, 0.5743863582611084, 0.14350247383117676, -0.3735086917877197, -0.6299927234649658, 0.5088682174682617, -0.6953752040863037, 0.23583650588989258], [0.25864362716674805, 0.5736973285675049, -0.3975222110748291, -0.6369199752807617, 0.5376672744750977, -0.19951462745666504, 0.6843924522399902, 0.6296660900115967, 0.36865997314453125, -0.7243289947509766, 0.5768749713897705, -0.5493001937866211, 0.31238412857055664, 0.21019506454467773, -0.368206262588501, -0.33148622512817383, -0.3421964645385742, -0.15616083145141602, 0.6617193222045898, 0.4400820732116699, 0.7893157005310059, -0.2935945987701416, 0.6241741180419922, -0.26036930084228516, -0.6958446502685547, 0.27047157287597656, -0.9095940589904785, 0.9525108337402344], [-0.5233585834503174, -0.45003342628479004, 0.15099048614501953, 0.6257956027984619, 0.9017877578735352, -0.18155455589294434, -0.20237135887145996, -0.014468908309936523, 0.01797318458557129, -0.5453977584838867, 0.21428155899047852, -0.9678947925567627, 0.5137600898742676, -0.1094369888305664, -0.13572359085083008, -0.1704423427581787, -0.9122319221496582, 0.8274900913238525, -0.11746454238891602, -0.8701446056365967, -0.9545385837554932, -0.6735866069793701, 0.9445557594299316, -0.3842940330505371, -0.6240942478179932, -0.1673595905303955, -0.3959221839904785, -0.05602693557739258], [0.8833198547363281, 0.14288711547851562, -0.9623878002166748, -0.26968836784362793, 0.9689288139343262, -0.3792128562927246, 0.2520296573638916, 0.1477947235107422, -0.24453139305114746, 0.94329833984375, 0.8014910221099854, 0.5443501472473145, 0.8486857414245605, -0.0795745849609375, -0.30250096321105957, -0.909733772277832, 0.8387842178344727, -0.41989898681640625, -0.8364224433898926, 0.04792976379394531, -0.38036274909973145, 0.12747883796691895, -0.5356688499450684, -0.04269552230834961, -0.2070469856262207, -0.6911153793334961, 0.33954668045043945, 0.25260138511657715], [0.3128373622894287, 0.36142778396606445, -0.2512378692626953, -0.6497259140014648, -0.21787405014038086, -0.9972476959228516, -0.026904821395874023, -0.4214746952056885, -0.3354766368865967, -0.6112637519836426, -0.7594058513641357, 0.09093379974365234, -0.7331845760345459, 0.5222046375274658, -0.8997514247894287, -0.3749384880065918, -0.0775001049041748, -0.26296448707580566, 0.404325008392334, -0.25776195526123047, 0.9136955738067627, 0.2623283863067627, -0.6411356925964355, 0.6646602153778076, -0.12833356857299805, -0.4184732437133789, -0.3663449287414551, -0.5468103885650635], [0.3770618438720703, 0.5572817325592041, -0.3657073974609375, -0.5056321620941162, 0.6555137634277344, 0.9557509422302246, -0.6900768280029297, -0.4980638027191162, 0.05510354042053223, -0.610318660736084, 0.9753992557525635, 0.7569930553436279, 0.4011664390563965, 0.8439173698425293, -0.5921270847320557, -0.2775266170501709, -0.061129093170166016, -0.49707984924316406, 0.5820951461791992, 0.008175849914550781, 0.06372833251953125, 0.3061811923980713, -0.5091361999511719, 0.9751057624816895, 0.4571402072906494, 0.6769094467163086, -0.46695923805236816, 0.44080281257629395], [-0.6510493755340576, -0.032715559005737305, 0.3482983112335205, -0.8135421276092529, 0.1506943702697754, 0.5220685005187988, -0.8834004402160645, -0.908900260925293, 0.3211519718170166, 0.896381139755249, -0.9448244571685791, -0.6193962097167969, -0.009401559829711914, 0.38227057456970215, -0.9219558238983154, -0.029483318328857422, -0.3889012336730957, 0.5242419242858887, 0.7338912487030029, -0.8713808059692383, -0.04948568344116211, -0.797940731048584, -0.9933724403381348, -0.262890100479126, -0.7165846824645996, -0.9763388633728027, -0.4105076789855957, 0.5907857418060303], [-0.6091890335083008, 0.7921168804168701, -0.033307790756225586, -0.9177074432373047, 0.4553513526916504, 0.5754055976867676, 0.6747269630432129, 0.0015664100646972656, -0.36865878105163574, -0.7999486923217773, 0.993431568145752, -0.7310445308685303, -0.49965715408325195, -0.028263330459594727, -0.20190834999084473, -0.7398116588592529, 0.10513901710510254, 0.22136950492858887, 0.42579007148742676, -0.4703383445739746, -0.8729751110076904, 0.28951215744018555, -0.3110074996948242, 0.9935362339019775, -0.29533815383911133, -0.3384673595428467, -0.07292437553405762, 0.8471579551696777], [-0.04648447036743164, -0.6876633167266846, -0.4921104907989502, -0.1925184726715088, -0.5843420028686523, -0.2852492332458496, 0.1251826286315918, -0.5709969997406006, 0.6744673252105713, 0.17812824249267578, 0.675086259841919, 0.1219022274017334, 0.6496286392211914, 0.05892682075500488, 0.33709263801574707, -0.9087743759155273, -0.4785141944885254, 0.2689247131347656, 0.3600578308105469, -0.6822943687438965, -0.0801839828491211, 0.9234893321990967, 0.5037875175476074, -0.8148105144500732, 0.6820621490478516, -0.8345451354980469, 0.9400079250335693, -0.752265453338623], [0.4599113464355469, 0.0292510986328125, -0.7475054264068604, -0.4074263572692871, 0.8800950050354004, 0.41760849952697754, 0.3225588798522949, 0.8359887599945068, -0.8655965328216553, 0.17258906364440918, 0.752063512802124, -0.48968982696533203, -0.9149389266967773, -0.46224403381347656, -0.26379919052124023, -0.9342350959777832, -0.5444085597991943, -0.4576752185821533, -0.12544608116149902, -0.3810274600982666, -0.5277583599090576, 0.3267025947570801, 0.4762594699859619, 0.09010529518127441, -0.2434844970703125, -0.8013439178466797, -0.23540687561035156, 0.8844473361968994], [-0.8922028541564941, -0.7912418842315674, -0.14429497718811035, -0.3925011157989502, 0.1870102882385254, -0.28865933418273926, 0.11481523513793945, -0.9174098968505859, -0.5264348983764648, -0.7296302318572998, 0.44644737243652344, 0.11140275001525879, 0.08105874061584473, 0.3871574401855469, -0.5030152797698975, -0.9560322761535645, -0.07085466384887695, 0.7949709892272949, 0.37600183486938477, -0.8664641380310059, -0.08428549766540527, 0.9169652462005615, 0.9479010105133057, 0.3576698303222656, 0.6677501201629639, -0.34919166564941406, -0.11635351181030273, -0.05966901779174805], [-0.9716870784759521, -0.7901370525360107, 0.9152195453643799, -0.42171406745910645, 0.20472931861877441, -0.9847748279571533, 0.9935972690582275, -0.5975158214569092, 0.9557573795318604, 0.41234254837036133, -0.26670074462890625, 0.869682788848877, 0.4443938732147217, -0.13968205451965332, -0.7745835781097412, -0.5692052841186523, 0.321591854095459, -0.3146944046020508, -0.3921670913696289, -0.36029601097106934, 0.33528995513916016, 0.029220104217529297, -0.8788590431213379, 0.6883881092071533, -0.8260040283203125, -0.43041515350341797, 0.42810845375061035, 0.40050792694091797], [0.6319584846496582, 0.32369279861450195, -0.6308813095092773, 0.07861590385437012, 0.5387494564056396, -0.902024507522583, -0.5346510410308838, 0.10787153244018555, 0.36048197746276855, 0.7801573276519775, -0.39187049865722656, 0.409869909286499, 0.5972449779510498, -0.7578165531158447, 0.30403685569763184, -0.7885205745697021, 0.01341390609741211, -0.023469209671020508, -0.11588907241821289, -0.941727876663208, -0.09618496894836426, 0.8042230606079102, 0.4683551788330078, -0.6497313976287842, 0.7443571090698242, 0.7150907516479492, -0.5759801864624023, -0.6523513793945312], [0.3150167465209961, -0.1853046417236328, 0.1839759349822998, -0.9234504699707031, -0.666614294052124, -0.740748405456543, 0.5700008869171143, 0.4091987609863281, -0.8912513256072998, 0.027419567108154297, 0.07219696044921875, -0.3128829002380371, 0.9465951919555664, 0.8715424537658691, -0.4559173583984375, -0.5862705707550049, -0.6734106540679932, 0.8419013023376465, -0.5523068904876709, -0.5019669532775879, -0.4969966411590576, -0.030994892120361328, 0.7572557926177979, 0.3824281692504883, 0.6366133689880371, -0.13271117210388184, 0.632627010345459, -0.9462625980377197], [-0.3923935890197754, 0.5466675758361816, -0.9815363883972168, -0.12867975234985352, 0.9932572841644287, -0.712486743927002, -0.17107725143432617, -0.41582536697387695, 0.10990118980407715, 0.11867499351501465, -0.7774863243103027, -0.9382553100585938, 0.4290587902069092, -0.1412363052368164, -0.498490571975708, 0.7793624401092529, 0.9015710353851318, -0.5107312202453613, 0.12394595146179199, 0.4988982677459717, -0.5731511116027832, -0.8105146884918213, 0.19758391380310059, 0.4081540107727051, -0.20432400703430176, 0.9924988746643066, -0.16952204704284668, 0.45574188232421875], [-0.023319005966186523, -0.3514130115509033, 0.4652390480041504, 0.7690563201904297, 0.7906622886657715, 0.9922001361846924, -0.6670932769775391, -0.5720524787902832, 0.3491201400756836, -0.18706512451171875, 0.4899415969848633, -0.5637645721435547, 0.8986928462982178, -0.7359066009521484, -0.6342356204986572, 0.6608924865722656, 0.6014213562011719, 0.7906208038330078, 0.19034814834594727, 0.16884255409240723, -0.8803558349609375, 0.4060337543487549, 0.9862797260284424, -0.48758840560913086, 0.3894319534301758, 0.4226539134979248, 0.00042724609375, -0.3623659610748291], [0.7065057754516602, -0.4103825092315674, 0.3343489170074463, -0.9341757297515869, -0.20749878883361816, -0.3589310646057129, -0.9470062255859375, 0.7851138114929199, -0.74678635597229, -0.05102086067199707, 0.16727972030639648, 0.12385678291320801, -0.41132497787475586, 0.5856695175170898, 0.06311273574829102, 0.8238284587860107, 0.2257852554321289, -0.6452250480651855, -0.6373245716094971, -0.1247873306274414, 0.0021851062774658203, -0.5648598670959473, 0.8261771202087402, 0.3713812828063965, -0.7185893058776855, 0.45911359786987305, 0.6722264289855957, -0.31804966926574707], [-0.2952606678009033, -0.12052011489868164, 0.9074821472167969, -0.9850583076477051, 0.6732273101806641, 0.7954013347625732, 0.938248872756958, -0.35915136337280273, -0.8291504383087158, 0.6020793914794922, -0.30096912384033203, 0.6136975288391113, 0.46443629264831543, -0.9057025909423828, 0.43993186950683594, -0.11653375625610352, 0.9514555931091309, 0.7985148429870605, -0.6911783218383789, -0.931948184967041, 0.06829452514648438, 0.711458683013916, 0.17953252792358398, 0.19076848030090332, 0.6339912414550781, -0.38822221755981445, 0.09893226623535156, -0.7663829326629639], [0.2640511989593506, 0.16821074485778809, 0.9845118522644043, 0.13789963722229004, -0.1097862720489502, 0.24889636039733887, 0.12135696411132812, 0.4419589042663574, -0.022361040115356445, 0.3793671131134033, 0.7053709030151367, 0.5814387798309326, 0.24962759017944336, -0.40136122703552246, -0.364804744720459, -0.2518625259399414, 0.25757312774658203, 0.6828348636627197, -0.08237361907958984, -0.07745933532714844, -0.9299273490905762, -0.3066704273223877, 0.22127842903137207, -0.6690163612365723, 0.7477891445159912, 0.5738682746887207, -0.9027633666992188, 0.33333301544189453], [0.44417595863342285, 0.5279359817504883, 0.36589932441711426, -0.049490928649902344, -0.3003063201904297, 0.8447706699371338, 0.8139019012451172, -0.4958505630493164, -0.3640005588531494, -0.7731854915618896, 0.4138674736022949, 0.3080577850341797, -0.5615301132202148, -0.4247474670410156, -0.25992918014526367, -0.7983508110046387, -0.4926283359527588, 0.08595061302185059, 0.9205574989318848, 0.6025278568267822, 0.37128734588623047, -0.1856670379638672, 0.9658422470092773, -0.6652145385742188, -0.2217710018157959, 0.8311929702758789, 0.9117603302001953, 0.4660191535949707], [-0.6164810657501221, -0.9509942531585693, 0.30228447914123535, 0.39792585372924805, -0.45194506645202637, -0.3315877914428711, 0.5393261909484863, 0.030223369598388672, 0.6013507843017578, 0.020318031311035156, 0.17352747917175293, -0.25470709800720215, -0.7904071807861328, 0.5383470058441162, -0.43855953216552734, -0.350492000579834, -0.5038156509399414, 0.0511777400970459, 0.9628784656524658, -0.520085334777832, 0.33083176612854004, 0.3698580265045166, 0.9121549129486084, -0.664802074432373, -0.45629024505615234, -0.44208550453186035, 0.6502475738525391, -0.597346305847168], [-0.5405080318450928, 0.2640984058380127, -0.2119138240814209, 0.04504036903381348, -0.10604047775268555, -0.8093295097351074, 0.20915007591247559, 0.08994936943054199, 0.5347979068756104, -0.550915002822876, 0.3008608818054199, 0.2416989803314209, 0.025292158126831055, -0.2790646553039551, 0.5850257873535156, 0.7020430564880371, -0.9527721405029297, 0.8273317813873291, -0.8028199672698975, 0.3686351776123047, -0.9391682147979736, -0.4261181354522705, 0.1674947738647461, 0.27993154525756836, 0.7567532062530518, 0.9245085716247559, 0.9245762825012207, -0.296356201171875], [-0.7747671604156494, 0.7632861137390137, 0.10236740112304688, 0.14044547080993652, 0.9318621158599854, -0.5622165203094482, -0.6605725288391113, -0.8286299705505371, 0.8717818260192871, -0.22177672386169434, -0.6030778884887695, 0.20917797088623047, 0.31551361083984375, 0.7741527557373047, -0.3320643901824951, -0.9014863967895508, 0.44268250465393066, 0.25649309158325195, -0.5621528625488281, -0.6077632904052734, 0.21485304832458496, -0.658627986907959, -0.9116294384002686, -0.294114351272583, 0.0452420711517334, 0.8542745113372803, 0.7148771286010742, 0.3244490623474121]]
# pylint: enable=line-too-long


def real_digit():
  return tf.expand_dims(tf.expand_dims(REAL_DIGIT, 0), -1)


def fake_digit():
  return tf.expand_dims(tf.expand_dims(FAKE_DIGIT, 0), -1)


def one_hot_real():
  return tf.constant(ONE_HOT)


def one_hot1():
  return tf.constant([[1.0] + [0.0] * 9])


def fake_logit_fn(tensor):
  batch_dim = tf.shape(tensor)[0]
  return tf.zeros([batch_dim, 10])


class MnistScoreTest(tf.test.TestCase):

  @mock.patch.object(util.tfhub, 'load', autospec=True)
  def test_any_batch_size(self, mock_tfhub_load):
    mock_tfhub_load.return_value = fake_logit_fn
    # Create a graph since placeholders don't work in eager execution mode.
    with tf.Graph().as_default():
      inputs = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])
      mscore = util.mnist_score(inputs)
      for batch_size in [4, 16, 30]:
        with self.cached_session() as sess:
          sess.run(
              mscore, feed_dict={inputs: np.zeros([batch_size, 28, 28, 1])})

  @mock.patch.object(util.tfhub, 'load', autospec=True)
  def test_deterministic(self, mock_tfhub_load):
    mock_tfhub_load.return_value = fake_logit_fn
    m_score = util.mnist_score(real_digit())
    with self.cached_session() as sess:
      m_score1 = sess.run(m_score)
      m_score2 = sess.run(m_score)
    self.assertEqual(m_score1, m_score2)

    with self.cached_session() as sess:
      m_score3 = sess.run(m_score)
    self.assertEqual(m_score1, m_score3)

  @mock.patch.object(util.tfhub, 'load', autospec=True)
  def test_single_example_correct(self, mock_tfhub_load):
    mock_tfhub_load.return_value = fake_logit_fn
    real_score = util.mnist_score(real_digit())
    fake_score = util.mnist_score(fake_digit())
    with self.cached_session() as sess:
      self.assertNear(1.0, sess.run(real_score), 1e-6)
      self.assertNear(1.0, sess.run(fake_score), 1e-6)

  def _disabled_test_minibatch_correct(self):
    """Tests the correctness of the mnist_score function."""
    # Disabled since it requires loading the tfhub MNIST module.
    mscore = util.mnist_score(
        tf.concat([real_digit(), real_digit(), fake_digit()], 0))
    with self.cached_session() as sess:
      self.assertNear(1.612828, sess.run(mscore), 1e-6)

  def _disabled_test_batch_splitting_doesnt_change_value(self):
    """Tests the correctness of mnist_score function over different batches."""
    # Disabled since it requires loading the tfhub MNIST module.
    for num_batches in [1, 2, 4, 8]:
      mscore = util.mnist_score(
          tf.concat([real_digit()] * 4 + [fake_digit()] * 4, 0),
          num_batches=num_batches)
      with self.cached_session() as sess:
        self.assertNear(1.649209, sess.run(mscore), 1e-6)


class MnistFrechetDistanceTest(tf.test.TestCase):

  @mock.patch.object(util.tfhub, 'load', autospec=True)
  def test_any_batch_size(self, mock_tfhub_load):
    mock_tfhub_load.return_value = fake_logit_fn
    # Create a graph since placeholders don't work in eager execution mode.
    with tf.Graph().as_default():
      inputs = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])
      fdistance = util.mnist_frechet_distance(inputs, inputs)
      for batch_size in [4, 16, 30]:
        with self.cached_session() as sess:
          sess.run(fdistance,
                   feed_dict={inputs: np.zeros([batch_size, 28, 28, 1])})

  @mock.patch.object(util.tfhub, 'load', autospec=True)
  def test_deterministic(self, mock_tfhub_load):
    mock_tfhub_load.return_value = fake_logit_fn
    fdistance = util.mnist_frechet_distance(
        tf.concat([real_digit()] * 2, 0),
        tf.concat([fake_digit()] * 2, 0))
    with self.cached_session() as sess:
      fdistance1 = sess.run(fdistance)
      fdistance2 = sess.run(fdistance)
    self.assertNear(fdistance1, fdistance2, 2e-1)

    with self.cached_session() as sess:
      fdistance3 = sess.run(fdistance)
    self.assertNear(fdistance1, fdistance3, 2e-1)

  @mock.patch.object(util.tfhub, 'load', autospec=True)
  def test_single_example_correct(self, mock_tfhub_load):
    mock_tfhub_load.return_value = fake_logit_fn
    fdistance = util.mnist_frechet_distance(
        tf.concat([real_digit()] * 2, 0),
        tf.concat([real_digit()] * 2, 0))
    with self.cached_session() as sess:
      self.assertNear(0.0, sess.run(fdistance), 2e-1)

  def _disabled_test_minibatch_correct(self):
    """Tests the correctness of the mnist_frechet_distance function."""
    # Disabled since it requires loading the tfhub MNIST module.
    fdistance = util.mnist_frechet_distance(
        tf.concat([real_digit(), real_digit(), fake_digit()], 0),
        tf.concat([real_digit(), fake_digit(), fake_digit()], 0))
    with self.cached_session() as sess:
      self.assertNear(43.5, sess.run(fdistance), 2e-1)

  def _disabled_test_batch_splitting_doesnt_change_value(self):
    """Tests correctness of mnist_frechet_distance function with batch sizes."""
    # Disabled since it requires loading the tfhub MNIST module.
    with tf.Graph().as_default():
      for num_batches in [1, 2, 4, 8]:
        fdistance = util.mnist_frechet_distance(
            tf.concat([real_digit()] * 6 + [fake_digit()] * 2, 0),
            tf.concat([real_digit()] * 2 + [fake_digit()] * 6, 0),
            num_batches=num_batches)
        with self.cached_session() as sess:
          self.assertNear(97.8, sess.run(fdistance), 2e-1)


class MnistCrossEntropyTest(tf.test.TestCase):

  @mock.patch.object(util.tfhub, 'load', autospec=True)
  def test_any_batch_size(self, mock_tfhub_load):
    mock_tfhub_load.return_value = fake_logit_fn
    # Create a graph since placeholders don't work in eager execution mode.
    with tf.Graph().as_default():
      num_classes = 10
      one_label = np.array([[1] + [0] * (num_classes - 1)])
      inputs = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])
      one_hot_label = tf.placeholder(tf.int32, shape=[None, num_classes])
      entropy = util.mnist_cross_entropy(inputs, one_hot_label)
      for batch_size in [4, 16, 30]:
        with self.cached_session() as sess:
          sess.run(entropy, feed_dict={
              inputs: np.zeros([batch_size, 28, 28, 1]),
              one_hot_label: np.concatenate([one_label] * batch_size)})

  @mock.patch.object(util.tfhub, 'load', autospec=True)
  def test_deterministic(self, mock_tfhub_load):
    mock_tfhub_load.return_value = fake_logit_fn
    xent = util.mnist_cross_entropy(real_digit(), one_hot_real())
    with self.cached_session() as sess:
      ent1 = sess.run(xent)
      ent2 = sess.run(xent)
    self.assertEqual(ent1, ent2)

    with self.cached_session() as sess:
      ent3 = sess.run(xent)
    self.assertEqual(ent1, ent3)

  def _disabled_test_single_example_correct(self):
    """Tests correctness of the mnist_cross_entropy function."""
    # Disabled since it requires loading the tfhub MNIST module.
    # The correct label should have low cross entropy.
    correct_xent = util.mnist_cross_entropy(real_digit(), one_hot_real())
    # The incorrect label should have high cross entropy.
    wrong_xent = util.mnist_cross_entropy(real_digit(), one_hot1())
    # A random digit should have medium cross entropy for any label.
    fake_xent1 = util.mnist_cross_entropy(fake_digit(), one_hot_real())
    fake_xent6 = util.mnist_cross_entropy(fake_digit(), one_hot1())
    with self.cached_session() as sess:
      self.assertNear(0.00996, sess.run(correct_xent), 1e-5)
      self.assertNear(18.63073, sess.run(wrong_xent), 1e-5)
      self.assertNear(2.2, sess.run(fake_xent1), 1e-1)
      self.assertNear(2.2, sess.run(fake_xent6), 1e-1)

  def _disabled_test_minibatch_correct(self):
    """Tests correctness of the mnist_cross_entropy function with batches."""
    # Disabled since it requires loading the tfhub MNIST module.
    # Reorded minibatches should have the same value.
    xent1 = util.mnist_cross_entropy(
        tf.concat([real_digit(), real_digit(), fake_digit()], 0),
        tf.concat([one_hot_real(), one_hot1(), one_hot1()], 0))
    xent2 = util.mnist_cross_entropy(
        tf.concat([real_digit(), fake_digit(), real_digit()], 0),
        tf.concat([one_hot_real(), one_hot1(), one_hot1()], 0))
    with self.cached_session() as sess:
      self.assertNear(6.972539, sess.run(xent1), 1e-5)
      self.assertNear(sess.run(xent1), sess.run(xent2), 1e-5)


class GetNoiseTest(tf.test.TestCase):

  def test_get_noise_categorical_syntax(self):
    util.get_eval_noise_categorical(
        noise_samples=4,
        categorical_sample_points=np.arange(0, 10),
        continuous_sample_points=np.linspace(-2.0, 2.0, 10),
        unstructured_noise_dims=62,
        continuous_noise_dims=2)

  def test_get_noise_continuous_dim1_syntax(self):
    util.get_eval_noise_continuous_dim1(
        noise_samples=4,
        categorical_sample_points=np.arange(0, 10),
        continuous_sample_points=np.linspace(-2.0, 2.0, 10),
        unstructured_noise_dims=62,
        continuous_noise_dims=2)

  def test_get_noise_continuous_dim2_syntax(self):
    util.get_eval_noise_continuous_dim2(
        noise_samples=4,
        categorical_sample_points=np.arange(0, 10),
        continuous_sample_points=np.linspace(-2.0, 2.0, 10),
        unstructured_noise_dims=62,
        continuous_noise_dims=2)

  def test_get_infogan_syntax(self):
    util.get_infogan_noise(
        batch_size=4,
        categorical_dim=10,
        structured_continuous_dim=3,
        total_continuous_noise_dims=62)


if __name__ == '__main__':
  tf.test.main()
