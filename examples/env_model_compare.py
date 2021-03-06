import gym
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from utils.gym_utils import generate_training_data
from test_torchgru import vGRU


model = vGRU()
print(model)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-2)

model.load_state_dict(torch.load('node_agent/sample_torchgru.pt'))
model.eval()

env = gym.make("Acrobot-v1")
states, actions, next_states = generate_training_data(env, 100)

print(states, actions, next_states)
input_data = torch.from_numpy(np.concatenate((states, actions), axis=1))
output_data = torch.from_numpy(next_states)

N = input_data.shape[0]
print(N)

data = []
for i in range(N):
    data.append((input_data[i], output_data[i]))

print(len(data))


y_env = output_data
y_model = torch.Tensor(y_env.shape)

with torch.no_grad():

    for i, (seq, y_train) in enumerate(data):

        seq = seq.float()
        if i > 0: seq[:6] = y_pred
        model.hidden = (torch.zeros(1, 1, model.hidden_size))

        y_pred = model(seq)
        y_model[i] = y_pred
        if i == 1: print(seq.shape, y_pred.shape, seq[:6], y_pred)
        # print(y_pred, y_train)

print('----------------')
print(y_model)
print('----------------')
print(y_env)
print('----------------')
print(type(y_model))
print(y_env.shape)
print(y_env[:, 1])

plt.plot(y_env[:, 0], 'b', marker="o", label="True")
plt.plot(y_model[:, 0], 'bx', label="RNN")

plt.plot(y_env[:, 1], 'g', marker="o", label="True")
plt.plot(y_model[:, 1], 'gx', label="RNN")

# plt.plot(y_env[:,2])
# plt.plot(y_model[:,2])

plt.legend()
# plt.savefig('Environment_GRU_compare.png')
plt.title("RNN Comparison of predicted and true trajectory over horizon of 50")
plt.xlabel("Horizon")
plt.ylabel("Position")
plt.show()
# if __name__ == '__main__':

#     ii = 0

#     model = LSTM()
#     criterion = nn.MSELoss()
#     optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)
#     end = time.time()

#     for itr in range(1, args.niters + 1):
#         optimizer.zero_grad()
#         batch_y0, batch_t, batch_y = get_batch()
#         pred_y = model.forward()
#         loss = criterion(pred_y, batch_y)
#         loss.backward()
#         optimizer.step()

#         time_meter.update(time.time() - end)
#         loss_meter.update(loss.item())

#         if itr % args.test_freq == 0:
#             with torch.no_grad():
#                 pred_y = model.forward()
#                 loss = criterion(pred_y, true_y)
#                 print('Iter {:04d} | Total Loss {:.6f}'.format(itr, loss.item()))
#                 visualize(true_y, pred_y, func, ii)
#                 ii += 1

#         end = time.time()
