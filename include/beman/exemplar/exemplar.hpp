// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#ifndef BEMAN_EXEMPLAR_EXEMPLAR_HPP
#define BEMAN_EXEMPLAR_EXEMPLAR_HPP

#include <beman/exemplar/config.hpp>

#if BEMAN_EXEMPLAR_USE_MODULES() && !defined(BEMAN_EXEMPLAR_INCLUDED_FROM_INTERFACE_UNIT)

import beman.exemplar;

#else

    #include <beman/exemplar/identity.hpp>

#endif // BEMAN_EXEMPLAR_USE_MODULES() &&
       // !defined(BEMAN_EXEMPLAR_INCLUDED_FROM_INTERFACE_UNIT)

#endif // BEMAN_EXEMPLAR_EXEMPLAR_HPP
