/* eslint-disable */
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
};

export type Flat = {
  __typename?: 'Flat';
  consumption: Scalars['Float'];
  humidity: Scalars['Float'];
  poweredBy: Scalars['Int'];
  temperature: Scalars['Float'];
};

export type Query = {
  __typename?: 'Query';
  hello: Scalars['String'];
};

export type State = {
  __typename?: 'State';
  flats: Array<Flat>;
  supplies: Array<Supply>;
};

export type Subscription = {
  __typename?: 'Subscription';
  getState: State;
};

export type Supply = {
  __typename?: 'Supply';
  consumptionPower: Scalars['Float'];
  efficiency: Scalars['Float'];
  generationPower: Scalars['Float'];
};
