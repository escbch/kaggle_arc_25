from typing import List, Optional
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

class TaskObject:
    def __init__(self, task_object: dict, is_test: bool = False):
        self.is_test = is_test
        self.input = np.array(task_object['input'])
        if not is_test:
            self.output = np.array(task_object['output'])

class Task:
    def __init__(self, task: dict, index: int, title: str):
        self.index = index
        self.title = title
        self.task_train = [TaskObject(task_object) for task_object in task['train']]
        self.task_test = [TaskObject(task_object, True) for task_object in task['test']]
        self.cmap = colors.ListedColormap(['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00', '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25'])
        self.norm = colors.Normalize(vmin=0, vmax=9)

    def _plot_one(self, ax, matrix: np.ndarray, train_or_test, input_or_output, solution=None, w=0.8):
        fs=12
        input_matrix = matrix.tolist()
        ax.imshow(input_matrix, cmap=self.cmap, norm=self.norm)

        #ax.grid(True, which = 'both',color = 'lightgrey', linewidth = 1.0)
        plt.setp(plt.gcf().get_axes(), xticklabels=[], yticklabels=[])
        ax.set_xticks([x-0.5 for x in range(1 + len(input_matrix[0]))])
        ax.set_yticks([x-0.5 for x in range(1 + len(input_matrix))])

        '''Grid:'''
        ax.grid(visible= True, which = 'both', color = '#666666', linewidth = w)

        ax.tick_params(axis='both', color='none', length=0)

        '''sub title:'''
        ax.set_title(train_or_test + ' ' + input_or_output, fontsize=fs, color = '#dddddd')

    def get_task_solutions(self, task_solutions: dict) -> List[np.ndarray]:
        """Get the solutions for the test cases of the task.

        Args:
            task_solutions (dict): Dictionary with the task solutions.

        Returns:
            np.ndarray: output matrix solving the corresponding test case.
        """
        solutions = []
        for solution_mat in task_solutions[self.title]:
            solutions.append(np.array(solution_mat))
        return solutions

    def plot_task(self, task_solutions: Optional[dict] = None, size=2.5, w1=0.9) -> None:
        """Plot the task challenges with test cases and the solutions for the test case if given.

        Args:
            task_solutions (Optional[dict]): the task solution if not given will not plot them. Defaults to None.
            size (float, optional): Size of the figure. Defaults to 2.5.
            w1 (float, optional): width of each figure. Defaults to 0.9.
        """
        title_size = 16
        num_train = len(self.task_train)
        num_test = len(self.task_test)

        wn = num_test + num_train
        fig, axs = plt.subplots(2, wn, figsize=(size * wn, 2 * size))
        plt.suptitle(f'Task #{self.index}, {self.title}', fontsize=title_size, fontweight='bold', y=1, color='#eeeeee')
        
        for j in range(num_train):
            self._plot_one(axs[0, j], self.task_train[j].input, 'train', 'input', w=w1)
            self._plot_one(axs[1, j], self.task_train[j].output, 'train', 'output', w=w1)

        if task_solutions is not None:
            solutions_matrices = self.get_task_solutions(task_solutions)
        for k in range(num_test):
            self._plot_one(axs[0, j+k+1], self.task_test[k].input, 'test', 'input', w=w1)
            if task_solutions is not None:
                self._plot_one(axs[1, j+k+1], solutions_matrices[k], 'test', 'output', w=w1)

        axs[1, j+1].set_xticklabels([])
        axs[1, j+1].set_yticklabels([])
        axs[1, j+1] = plt.figure(1).add_subplot(111)
        axs[1, j+1].set_xlim([0, wn])

        colorSeparator = 'white'
        for m in range(1, wn):
            axs[1, j+1].plot([m,m],[0,1],'--', linewidth=1, color = colorSeparator)
        axs[1, j+1].plot([num_train,num_train],[0,1],'-', linewidth=3, color = colorSeparator)

        axs[1, j+1].axis("off")

        fig.patch.set_linewidth(5) #widthframe
        fig.patch.set_edgecolor('black') #colorframe
        fig.patch.set_facecolor('#444444') #background
    
        plt.tight_layout()

        print(f'#{self.index}, {self.title}') # for fast and convinience search
        plt.show()

class Tasks:
    def __init__(self, challenge: dict):
        self.tasks = [Task(challenge[task], i, task) for i, task in enumerate(list(challenge))]

    def get_task(self, index: int) -> Task:
        return self.tasks[index]