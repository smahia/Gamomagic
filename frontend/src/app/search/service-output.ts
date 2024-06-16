// Output returned from the service (REST API)
export interface Game {
  game_code: number;
  game_name: string;
  game_platform: string;
  game_region: string;
  game_language: string;
}

export class GameImpl implements Game {
  game_code: number;
  game_name: string;
  game_platform: string;
  game_region: string;
  game_language: string;

  constructor() {
    this.game_code = 0;
    this.game_name = '';
    this.game_platform = '';
    this.game_region = '';
    this.game_language = '';
  }
}
