#!/usr/bin/env python
import os

COV = None
if os.environ.get("FLASK_COVERAGE"):
    import coverage
    COV = coverage.coverage(branch=True, include='powertrain/*')
    COV.start()

from powertrain import create_app, db
from powertrain.models import DerivedBehavior, RawBehavior, Configuration,\
    DerivedImage, RawImage, Job, ExecutionUnit, JobSetup, JobTeardown,\
    MRSession, Project, Scan, Task, TaskSetup, TaskTeardown, User
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app,
                db=db,
                DerivedBehavior=DerivedBehavior,
                RawBehavior=RawBehavior,
                Configuration=Configuration,
                DerivedImage=DerivedImage,
                RawImage=RawImage,
                Job=Job,
                ExecutionUnit=ExecutionUnit,
                JobSetup=JobSetup,
                JobTeardown=JobTeardown,
                MRSession=MRSession,
                Project=Project,
                Scan=Scan,
                Task=Task,
                TaskSetup=TaskSetup,
                TaskTeardown=TaskTeardown,
                User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=1).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print("Coverage summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print("HTML version: file://{}/index.html".format(covdir))
        COV.erase()



if __name__ == '__main__':
    manager.run()
