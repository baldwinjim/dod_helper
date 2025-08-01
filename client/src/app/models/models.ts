export interface Speaker {
  name: string;
  picture: string;
  linkedin: string;
  twitter: string;
  website: string;
  bio: string;
  talkType: string;
  talkTitle: string;
  talkSynopsis: string;
  talkLink: string;
}

/*
Speaker Example:
{
    "name": "James Thomas",
    "picture": "james-thomas.png",
    "linkedin": "https://www.linkedin.com/in/thatjamesthomas/",
    "twitter": "jamesthomas",
    "website": "",
    "bio": "James has been a lifelong enthusiast of technology, and has been lucky enough to be paid to tinker with it for the past 15 years or so. He in particular has a fondness for infrastructure and CI/CD pipelines, which when given the proper care are oftentimes the unsung hero of any successful delivery team.\n\nIn his spare time you can find James taking his young daughters to the park, playing board games with friends and family, or working on the seemingly endless home improvement projects he finds himself doing.",
    "talkType": "lightning",
    "talkTitle": "Docker Bake is Pretty Great",
    "talkSynopsis": "Docker Bake is a newly GA feature of the Docker ecosystem. It provides an HCL-based (with yaml and json options) DSL for defining the parameters of your container build. It also provides some really handy features around parameter validation, so you can clearly communicate to users what things you expect them to provide. On top of that, it includes matrix support to make it significantly easier to build a slew of containers off of a single definition.\n\nNone of these things by themselves are revolutionary, but when packaged together and included by default they provide a whole lot of convenience without much of a barrier to entry. I’ve simplified the builds of numerous pipelines with Docker Bake, and if you spend as much time caring for containers as I do I think you’ll like it quite a bit.",
    "talkLink": "james-thomas"
}
*/

export interface Sponsor {
  company: string;
  contactName: string;
  contanctEmail: string;
}
