'use client';
import { Disclosure} from '@headlessui/react'
import React, { createContext } from 'react';


const navigation = [
  { name: 'Sequential', href: '#', current: true },
  { name: 'Concurrent', href: '#', current: false },
]

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Navbar() {
  return (
    <Disclosure as="nav">
      {({ open }) => (
          <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
            <p className="flex items-center justify-center text-white font-bold">Web Scraping Strategy</p>
            <div className="relative h-10 items-center justify-between">
              <div className="flex flex-1 items-center justify-center">
                  <div className="flex space-x-4">
                  {navigation.map((item) => (
                    <a
                      key={item.name}
                      href={item.href}
                      className={classNames(
                        item.current
                          ? (item.name === 'Sequential'
                              ? ' text-yellow-1 text-xs hover:text-yellow-2 duration-300'
                              : ' text-purple-500 text-xs')
                          : 'text-grey-1 hover:text-white text-xs duration-300'
                      )}
                        aria-current={item.current ? 'page' : undefined}
                      >
                        {item.name}
                      </a>
                    ))}
                  </div>
              </div>
            </div>
          </div>
      )}
    </Disclosure>
  )
}
