import numpy as np

from gym.envs.mujoco import HumanoidEnv as HumanoidEnv

def mass_center(model, sim):
    mass = np.expand_dims(model.body_mass, 1)
    xpos = sim.data.xipos
    return (np.sum(mass * xpos, 0) / np.sum(mass))


class HumanoidDirEnv(HumanoidEnv):

    def __init__(self, goal=None):
        if goal is None:
            goal = 1
        self._goal = goal
        super(HumanoidDirEnv, self).__init__()

    def step(self, action):
        pos_before = np.copy(mass_center(self.model, self.sim)[:2])
        self.do_simulation(action, self.frame_skip)
        pos_after = mass_center(self.model, self.sim)[:2]

        alive_bonus = 5.0
        data = self.sim.data
        goal_direction = (np.cos(self._goal), np.sin(self._goal))
        lin_vel_cost = 0.25 * np.sum(goal_direction * (pos_after - pos_before)) / self.model.opt.timestep
        quad_ctrl_cost = 0.1 * np.square(data.ctrl).sum()
        quad_impact_cost = .5e-6 * np.square(data.cfrc_ext).sum()
        quad_impact_cost = min(quad_impact_cost, 10)
        reward = lin_vel_cost - quad_ctrl_cost - quad_impact_cost + alive_bonus
        qpos = self.sim.data.qpos
        done = bool((qpos[2] < 1.0) or (qpos[2] > 2.0))

        return self._get_obs(), reward, done, dict(reward_linvel=lin_vel_cost,
                                                   reward_quadctrl=-quad_ctrl_cost,
                                                   reward_alive=alive_bonus,
                                                   reward_impact=-quad_impact_cost,
                                                   achieved=(pos_after - pos_before) / self.model.opt.timestep)

    def _get_obs(self):
        data = self.sim.data
        return np.concatenate([data.qpos.flat[2:],
                               data.qvel.flat,
                               data.cinert.flat,
                               data.cvel.flat,
                               data.qfrc_actuator.flat,
                               data.cfrc_ext.flat])

    def sample_goals(self, exp_mode):
        if exp_mode == 'normal':
            train_goals = np.random.uniform(0., 1.5, size=(32,)) * np.pi
            wd_goals = np.random.uniform(0., 1.5, size=(8,)) * np.pi
            ood_goals = np.random.uniform(1.5, 2.0, size=(8,)) * np.pi
        else:
            raise NotImplementedError

        return train_goals, wd_goals, ood_goals

    def set_goal(self, goal):
        self._goal = goal
        self.reset()
