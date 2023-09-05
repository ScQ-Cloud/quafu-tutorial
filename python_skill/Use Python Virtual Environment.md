# Use Python Virtual Environment

To avoid version or dependence conflicts, we often create a virtual environment (``venv``) for a complex python project. It is also suggested to do so when you get started with ``pyquafu-tutorial``. If you are beginners for ``python``, the following instructions may be helpful to you.

Firstly make sure there is a suitable version of [python](https://www.python.org/downloads/) on your computer, and note that ``pyquafu`` is tested for ``python>=3.8``. You do not have to install heavy IDE like ``PyCharm``. The next step is to open Command Line or Terminal, enter the path where you want to store the ``venv``, and create it by

```bash
python -m venv <venv-name>
```

Here you are free to choose ``<venv-name>`` you like. Enter the environment by 

```bash
<venv-name>\Scripts\activate
```

Then you may play with ``python`` and ``pyquafu``. When you finish your work, to deactivate the ``venv``, just execute

```bash
deactivate
```

