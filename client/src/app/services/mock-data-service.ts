import { Injectable } from '@angular/core';
import { Speaker, Sponsor } from '../models/models';

@Injectable({
  providedIn: 'root',
})
export class MockDataService {
  public speakers: Speaker[] = [
    {
      name: 'James Thomas',
      picture: 'james-thomas.png',
      linkedin: 'https://www.linkedin.com/in/thatjamesthomas/',
      twitter: 'jamesthomas',
      website: '',
      bio: 'James has been a lifelong enthusiast of technology, and has been lucky enough to be paid to tinker with it for the past 15 years or so. He in particular has a fondness for infrastructure and CI/CD pipelines, which when given the proper care are oftentimes the unsung hero of any successful delivery team.\n\nIn his spare time you can find James taking his young daughters to the park, playing board games with friends and family, or working on the seemingly endless home improvement projects he finds himself doing.',
      talkType: 'lightning',
      talkTitle: 'Docker Bake is Pretty Great',
      talkSynopsis:
        'Docker Bake is a newly GA feature of the Docker ecosystem. It provides an HCL-based (with yaml and json options) DSL for defining the parameters of your container build. It also provides some really handy features around parameter validation, so you can clearly communicate to users what things you expect them to provide. On top of that, it includes matrix support to make it significantly easier to build a slew of containers off of a single definition.\n\nNone of these things by themselves are revolutionary, but when packaged together and included by default they provide a whole lot of convenience without much of a barrier to entry. I’ve simplified the builds of numerous pipelines with Docker Bake, and if you spend as much time caring for containers as I do I think you’ll like it quite a bit.',
      talkLink: 'james-thomas',
    },
    {
      name: 'Aisha Patel',
      picture: 'aisha-patel.jpg',
      linkedin: 'https://www.linkedin.com/in/aishapatel/',
      twitter: 'aisha_codes',
      website: 'https://aishapatel.dev',
      bio: 'Aisha is a full-stack developer and conference speaker with a passion for clean architecture and developer education.',
      talkType: 'full',
      talkTitle: 'Design Systems that Scale',
      talkSynopsis:
        'This talk explores how to build and maintain scalable design systems that keep teams aligned and interfaces consistent.',
      talkLink: 'aisha-patel',
    },
    {
      name: 'Carlos Méndez',
      picture: 'carlos-mendez.jpg',
      linkedin: 'https://www.linkedin.com/in/carlosmendez/',
      twitter: 'carlosm_dev',
      website: '',
      bio: 'Carlos is a DevOps engineer who loves automation and teaching others how to simplify complex workflows with pipelines and infrastructure-as-code.',
      talkType: 'lightning',
      talkTitle: 'From Bash to GitHub Actions',
      talkSynopsis:
        'Learn how to convert legacy scripts into modern, modular CI/CD pipelines using GitHub Actions and reusable workflows.',
      talkLink: 'carlos-mendez',
    },
  ];
  public sponsors: Sponsor[] = [];
}
