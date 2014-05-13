#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_relations.py

Test relationships between models
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'


from powertrain.models import Project, User, MRSession, Configuration, \
    Task, TaskSetup, TaskTeardown, Job, JobSetup, JobTeardown, \
    DerivedImage, DerivedBehavior, RawImage, RawBehavior, ExecutionUnit, Scan, \
    RawRender, DerivedRender

from tests import PowertrainTestBase

class ModelTestCase(PowertrainTestBase):

    def test_user_to_project(self):
        p = Project(name='test')
        u = User(email='foo@bar.bat')
        self.commit(p, u)
        u.projects.append(p)
        self.assertIn(u, p.users)

    def test_project_to_user(self):
        p = Project(name='test')
        u = User(email='foo@bar.bat')
        self.commit(p, u)
        p.users.append(u)
        self.assertIn(p, u.projects)

    def test_session_to_project(self):
        p = Project(name='test')
        sess1 = MRSession(name=1, project=p)
        sess2 = MRSession(name=2, project=p)
        self.commit(p, sess1, sess2)
        self.assertIn(sess1, p.mrsessions)
        self.assertEqual(len(p.mrsessions), 2)

    def test_task_to_project(self):
        p = Project(name='test')
        t1 = Task(name="Cortical Reconstruction", project=p)
        t2 = Task(name="fMRI Model", project=p)
        self.commit(p, t1, t2)
        self.assertEqual(len(p.tasks), 2)
        self.assertIn(t2, p.tasks)

    def test_config_to_task(self):
        t = Task(name="Freesurfer")
        c = Configuration(name="Freesurfer")
        c.tasks.append(t)
        self.commit(t, c)
        self.assertIn(c, t.configurations)

    def test_task_to_config(self):
        t1 = Task(name="Freesurfer")
        t2 = Task(name="Tractography")
        c1 = Configuration(name="Freesurfer")
        c2 = Configuration(name="FSL")
        self.commit(t1, t2, c1, c2)
        t1.configurations.append(c1)
        t2.configurations.extend([c1, c2])
        self.assertIn(t1, c1.tasks)
        self.assertEqual(len(t2.configurations), 2)

    def test_task_to_task(self):
        p = Project(name="test")
        t1 = Task(name="Probtrack", project=p)
        t2 = Task(name="Recon", project=p, parent=t1)
        t3 = Task(name="BedpostX", project=p, parent=t1)
        t4 = Task(name="DTIQA", project=p, parent=t3)
        self.commit(p, t1, t2, t3)

        self.assertIn(t4, t3.children)
        self.assertEqual(len(t1.children), 2)

    def test_scan_to_session(self):
        sess = MRSession(name=1)
        scan1 = Scan(name="Foo_1_Improved_3D", mrsession=sess)
        scan2 = Scan(name="Foo_1_HARDI", mrsession=sess)
        self.commit(sess, scan2)
        self.assertIn(scan1, sess.scans)
        self.assertEqual(len(sess.scans), 2)

    def test_rawimage_to_scan(self):
        scan = Scan(name="Foo_1_Improved_3D")
        image1 = RawImage(name="Foo_1_01_Improved_3D", scan=scan)
        image2 = RawImage(name="Foo_1_02_Improved_3D", scan=scan)
        self.commit(scan, image1, image2)

        self.assertEqual(len(scan.rawimages), 2)
        self.assertIn(image1, scan.rawimages)

    def test_rawbehavior_to_scan(self):
        scan = Scan(name="Foo_1_Improved_3D")
        rawbehav1 = RawBehavior(name="edat1", scan=scan)
        rawbehav2 = RawBehavior(name="edat2", scan=scan)
        self.commit(scan, rawbehav1, rawbehav2)

        self.assertEqual(len(scan.rawbehaviors), 2)
        self.assertIn(rawbehav1, scan.rawbehaviors)

    def test_rawrender_to_rawimage(self):
        image = RawImage(name="Foo_1_01_Improved_3D")
        render1 = RawRender(name="Foo_1_01_Improved_3D.jpg", image=image)
        render2 = RawRender(name="Foo_1_01_Improved_3D.png", image=image)
        self.commit(image, render1, render2)

        self.assertEqual(len(image.renders), 2)
        self.assertIn(render1, image.renders)

    def test_derivedrender_to_derivedimage(self):
        image = DerivedImage(name="T1_bet")
        render1 = DerivedRender(name="T1_bet.png", image=image)
        render2 = DerivedRender(name="T1_bet_overlay.png", image=image)
        self.commit(image, render1, render2)

        self.assertEqual(len(image.renders), 2)
        self.assertIn(render1, image.renders)

    def test_derivedbehavior_to_job(self):
        job = Job(name='Analyze Behav')
        db1 = DerivedBehavior(name='task accuracy')
        db1.jobs.append(job)
        db2 = DerivedBehavior(name='task timing')
        db2.jobs.append(job)
        self.commit(job, db1, db2)
        self.assertEqual(len(job.derived_behaviors), 2)
        self.assertIn(db1, job.derived_behaviors)

    def test_teardown_to_job(self):
        job = Job(name="SPM")
        td1 = JobTeardown(name="motion to redcap", job=job)
        td2 = JobTeardown(name="email", job=job)
        self.commit(job, td1, td2)
        self.assertEqual(len(job.teardowns), 2)
        self.assertIn(td2, job.teardowns)

    def test_setup_to_job(self):
        job = Job(name="SPM")
        su1 = JobSetup(name="unarchive", job=job)
        su2 = JobSetup(name="gunzip", job=job)
        self.commit(job, su1, su2)
        self.assertEqual(len(job.setups), 2)
        self.assertIn(su1, job.setups)

    def test_teardown_to_task(self):
        task = Task(name="Task")
        td1 = TaskTeardown(name="Teardown1", task=task)
        td2 = TaskTeardown(name="Teardown2", task=task)
        self.commit(task, td1, td2)
        self.assertEqual(len(task.teardowns), 2)
        self.assertIn(td1, task.teardowns)

    def test_setup_to_task(self):
        task = Task(name="Task")
        su1 = TaskSetup(name="setup1", task=task)
        su2 = TaskSetup(name="setup2", task=task)
        self.commit(task, su1, su2)
        self.assertEqual(len(task.setups), 2)
        self.assertIn(su2, task.setups)

    def test_eu_to_job(self):
        job = Job(name="Job")
        eu1 = ExecutionUnit(name="Preproc", job=job)
        eu2 = ExecutionUnit(name="1st-Level", job=job)
        self.commit(job, eu1, eu2)
        self.assertEqual(len(job.execution_units), 2)
        self.assertIn(eu1, job.execution_units)
        self.assertEqual(job, eu1.job)
